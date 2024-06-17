from loguru import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ContextTypes, CallbackContext

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import prompts
from src.states import UserStateEnum, UserStates

from random import choice

import json

ITEMS_PER_PAGE = 5
TOTAL_CSV = ""
RECOM_JSON = ""

with open(RECOM_JSON, "r") as fin:
    recoms = json.load(fin)

recom_items = [
    (f"""{item_row + 1}. {item["name"]}
Сумма: {item["Цена ГК, руб."]}
""", item["Объяснение"])
    for item_row, item in enumerate(recoms) # Объяснение
]

user_state = UserStates()
total_df = pd.read_csv(TOTAL_CSV)
items_name = total_df["0"].to_list()

def find_most_similar(user_prompt, item_names):
    # Combine the user prompt and item names into one list
    all_texts = [user_prompt] + item_names
    
    # Initialize the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the text data into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarity between the user prompt and item names
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Find the index of the most similar item
    most_similar_index = similarities.argmax()
    
    return item_names[most_similar_index]

def make_remains_plot(item_name: str):
    item_data = total_df[total_df["0"] == item_name].fillna(0).iloc[0].to_list()

    # Data
    quarters = ['1Q', '2Q', '3Q', '4Q']
    zakupki = [item_data[4], item_data[12], item_data[20], item_data[28]]
    zatraty = [item_data[6], item_data[14], item_data[22], item_data[30]]
    ostaki = [item_data[8], item_data[16], item_data[24], item_data[32]]

    logger.info(zakupki)
    logger.info(zatraty)
    logger.info(ostaki)

    bar_width = 0.2
    x = np.arange(len(quarters))

    # Plotting
    fig, ax = plt.subplots()
    bars1 = ax.bar(x - bar_width, ostaki, bar_width, label='Остатки', color='#A52A2A')
    bars2 = ax.bar(x, zakupki, bar_width, label='Закупки', color='#F08080')
    bars3 = ax.bar(x + bar_width, zatraty, bar_width, label='Затраты', color='#FFDAB9')

    # Adding titles and labels
    ax.set_title('Остатки товара')
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    ax.legend()

    # Show the plot
    filename = f"./plots/{datetime.now()}_{item_name[:10]}.png"
    plt.savefig(filename)

    return filename


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state.update_state(update)
    chat_id = update.effective_chat.id
    logger.info(f"START with {chat_id}")

    username = update.message.from_user.username
    # проверка есть ли у нас такой ник
    # если нет
    # await context.bot.send_message(
    #     chat_id=chat_id, text=prompts.AUTH_NO
    # )

    await context.bot.send_message(
        chat_id=chat_id, text=prompts.GREETING_TEXT
    )

    # проверка есть ли дата по компании

    await ask_choice(update, context)


async def ask_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Посмотреть остатки", callback_data="remains"),
            ],
            [
                InlineKeyboardButton("Получить прогноз", callback_data="forecast"),
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=prompts.ASK_FOR_CHOICE,
        reply_markup=reply_markup,
    )

async def ask_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите товар:"
    )

async def got_to_web_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Более побробная информация в нашем веб-сервисе: http://glavcontrol.dev-stand.com"
    )


async def send_remains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = user_state.get_state(update)
    if status == UserStateEnum.START:
        await ask_item(update, context)
        user_state.update_state(update, UserStateEnum.REMAINS)
    elif status == UserStateEnum.REMAINS:
        # user_prompt = "бумага офисная"
        logger.info(f"Remains for {update.message.text}")
        item_names = items_name

        most_similar_item = find_most_similar(update.message.text, item_names)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Найденный товар: {most_similar_item}"
        )

        plot_filename = make_remains_plot(most_similar_item)
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=open(plot_filename, 'rb'))


def get_paginated_text(page: int) -> str:
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_items = recom_items[start_idx:end_idx]
    
    text = "\n".join([x[0] + f"Обоснование: {choice(x[1])}\n" for x in page_items])
    return text

def get_navigation_keyboard(page: int) -> InlineKeyboardMarkup:
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton('⬅️', callback_data=f'page_{page-1}'))
    if (page + 1) * ITEMS_PER_PAGE < len(recom_items):
        navigation_buttons.append(InlineKeyboardButton('➡️', callback_data=f'page_{page+1}'))

    return InlineKeyboardMarkup([navigation_buttons, [InlineKeyboardButton("Создать заявку", callback_data=f'create_order')]])

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith('page_'):
        page = int(query.data.split('_')[1])
        
        await query.edit_message_text('*Товары:*\n\n' + get_paginated_text(page),
                                      reply_markup=get_navigation_keyboard(page),
                                      parse_mode=constants.ParseMode.MARKDOWN)
        
    elif query.data == "create_order":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Создать заявку можно в нашем веб-сервисе: http://glavcontrol.dev-stand.com"
        )
        await ask_choice(update, context)
    elif query.data == "remains":
        await send_remains(update, context)

    elif query.data == "forecast":
        await send_forecast(update, context)

async def send_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # status = user_state.get_state(update)
    # if status == UserStateEnum.START:
    #     await ask_item(update, context)
    user_state.update_state(update, UserStateEnum.FORECAST)
    # elif status == UserStateEnum.FORECAST:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='*Товары:*\n\n' + get_paginated_text(0), 
        reply_markup=get_navigation_keyboard(0),
        parse_mode=constants.ParseMode.MARKDOWN)


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = user_state.get_state(update)
    if status == UserStateEnum.REMAINS:
        await send_remains(update, context)
    elif status == UserStateEnum.FORECAST:
        await send_forecast(update, context)
        # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/Users/kirakuznetsova/Desktop/GLAVControl/forecast.png', 'rb'))
        
    await got_to_web_service(update, context)
    user_state.update_state(update, UserStateEnum.START)
    await ask_choice(update, context)
