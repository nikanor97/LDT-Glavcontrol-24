from loguru import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ContextTypes, CallbackContext

from random import choice
import json
import psycopg2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import prompts
from src.states import UserStateEnum, UserStates
from settings import settings

recom_filename_dict = {
    "year": settings.recom_year_json_filepath,
    "q1": settings.recom_q1_json_filepath,
    "q2": settings.recom_q2_json_filepath,
    "q3": settings.recom_q3_json_filepath,
    "q4": settings.recom_q4_json_filepath
}

recom_dict = {}
for time, file_path in recom_filename_dict.items():
    with open(file_path, "r") as fin:
        recom_dict[time] = json.load(fin)

recom_items_dict = {}
for time, recoms in recom_dict.items():
    
    recom_items = [
        (f"""*{item_row + 1}. {item["name"]}*
Цена: {item["price"] /  item["amount"]}
Количество: { item["amount"]}
Сумма: {item["price"]}
""", item["Объяснение"])
        for item_row, item in enumerate(recoms) # Объяснение
    ]

    recom_items_dict[time] = recom_items

user_state = UserStates()
total_df = pd.read_csv(settings.total_csv_filepath)
items_name = total_df["0"].to_list()

with open(settings.kontract_names_json_filepath, "r") as fin:
    kontract_item_names = json.load(fin)

def db_request(query: str, db_name: str):
    try:
        connection = psycopg2.connect(
            database=db_name,
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            port=settings.db_port)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error while fetching data from PostgreSQL {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()

    return result

def find_most_similar(user_prompt, item_names):
    all_texts = [user_prompt] + item_names
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    most_similar_index = similarities.argmax()
    
    return item_names[most_similar_index]

def get_top_n_similar_products(user_input, items, n=5):
    all_items = items + [user_input]
    vectorizer = TfidfVectorizer().fit_transform(all_items)
    cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
    top_n_indices = cosine_similarities.argsort()[-n:][::-1]

    return [items[i] for i in top_n_indices]

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

def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username

    q = f"""select * 
from public.users u 
where u.telegram_username is not null and u.telegram_username = '{username.lower()}'"""
    
    user = db_request(q, settings.db_name_users)

    return user

def get_company_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = f"""select *
from public.companies c 
join public.user_companies uc on c.id = uc.company_id 
where uc.user_id = '{user_state.get_uuid(update)}'"""
    
    company_info = db_request(q, settings.db_name_projects)

    return company_info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state.update_state(update)
    chat_id = update.effective_chat.id
    logger.info(f"START with {chat_id}")

    user = check_user(update, context)

    if not user:
        await context.bot.send_message(
            chat_id=chat_id, text=prompts.AUTH_NO
        )

    else:
        user_state.update_nickname(update, user[0][4].lower())
        user_state.update_uuid(update, user[0][0])
        await context.bot.send_message(
            chat_id=chat_id, text=prompts.GREETING_TEXT
        )

        # проверка есть ли дата по компании

        await ask_choice(update, context)

async def ask_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state.update_state(update, UserStateEnum.START)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Основная информация", callback_data="about_company"),
            ],
            [
                InlineKeyboardButton("Статистика компании", callback_data="stats"),
            ],
            [
                InlineKeyboardButton("Посмотреть остатки", callback_data="remains"),
            ],
            [
                InlineKeyboardButton("Получить прогноз", callback_data="forecast"),
            ],
            [
                InlineKeyboardButton("Посмотреть заявки", callback_data="applications"),
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=prompts.ASK_FOR_CHOICE,
        reply_markup=reply_markup,
    )

async def about_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    company_info = get_company_info(update, context)[0]

    company_name = company_info[1]
    company_region = company_info[2]
    company_inn = company_info[3]
    company_director = company_info[5]
    company_date = company_info[6]
    company_ogrn = company_info[4]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""*О компании:*

*Наименование:* {company_name}
*Регион:* {company_region}
*Директор:* {company_director}
*Дата основания:* {company_date.strftime('%d.%m.%Y')}
*ИНН:* {company_inn}
*ОГРН:* {company_ogrn}""",
        parse_mode=constants.ParseMode.MARKDOWN
    )

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""*Основная статистика:*

*Сумма размещенных контрактов:*
138 697 000 000 рублей
*Дата последнего контракта:*
29.12.2022
*Самый дорогой товар:*
Сертификат на техническую поддержку информационно-технологического оборудования — 749962342.38 рублей
*Самая дорогая услуга:*
Услуги по предоставлению программного обеспечения, инженерной, вычислительной и информационно-телекоммуникационной инфраструктуры центров обработки данных, шт — 1453720391.58 рублей""",
        parse_mode=constants.ParseMode.MARKDOWN
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
        logger.info(f"Remains for {update.message.text}")
        item_names = items_name

        most_similar_item = find_most_similar(update.message.text, item_names)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"*Информация об остатках:*\n\nНайденный товар: {most_similar_item}",
            parse_mode=constants.ParseMode.MARKDOWN
        )

        plot_filename = make_remains_plot(most_similar_item)
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=open(plot_filename, 'rb'))

def get_paginated_text(page: int, items: list) -> str:
    start_idx = page * settings.forecast_items_per_page
    end_idx = start_idx + settings.forecast_items_per_page
    page_items = items[start_idx:end_idx]
    
    text = "\n".join([x[0] + f"Обоснование: {choice(x[1])}\n" for x in page_items])
    return text

def get_navigation_keyboard(page: int, items: list) -> InlineKeyboardMarkup:
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton('⬅️', callback_data=f'page_{page - 1}'))
    if (page + 1) * settings.forecast_items_per_page < len(items):
        navigation_buttons.append(InlineKeyboardButton('➡️', callback_data=f'page_{page + 1}'))

    return InlineKeyboardMarkup([navigation_buttons, [InlineKeyboardButton("Создать заявку", callback_data=f'create_order')]])

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith('page_'):
        page = int(query.data.split('_')[1])
        items = recom_items_dict[user_state.get_attr(update, "time")]
        
        await query.edit_message_text('*Товары:*\n\n' + get_paginated_text(page, items),
                                      reply_markup=get_navigation_keyboard(page, items),
                                      parse_mode=constants.ParseMode.MARKDOWN)
        
    elif query.data == "create_order":
        time = user_state.get_attr(update, "time")
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(recom_filename_dict[time], 'rb')
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Более подробная информация в нашем веб-сервисе: http://glavcontrol.dev-stand.com"
        )
        await ask_choice(update, context)

    elif query.data == "remains":
        await send_remains(update, context)

    elif query.data == "forecast":
        await send_forecast(update, context)

    elif query.data == "forecast_all_goods":
        await send_full_forecast(update, context)

    elif query.data in ("forecast_all_goods_year", "forecast_all_goods_q1",
                        "forecast_all_goods_q2", "forecast_all_goods_q3", "forecast_all_goods_q4"):
        await send_full_forecast(update, context, query.data.split("_")[-1])

    elif query.data == "forecast_specific_good":
        await send_specific_forecast(update, context)

    elif query.data.startswith("good_"):
        await send_specific_forecast(update, context, int(query.data.split("_")[-1]))

    elif query.data in ("forecast_specific_good_year", "forecast_specific_good_q1", 
                        "forecast_specific_good_q2", "forecast_specific_good_q3", "forecast_specific_good_q4"):
        
        time = query.data.split("_")[-1]

        good_recs = user_state.get_attr(update, "good_recs")

        if good_recs[time]:

        
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"""*Прогноз:*

*Наименование:* {good_recs[time][0]["name"]}
*Тип:* {"Товар" if good_recs[time][0]["type"] == "item" else "Услуга"}
*Цена:* {round(good_recs[time][0]["price"] / good_recs[time][0]["amount"], 2)}
*Количество:* {good_recs[time][0]["amount"]}
*Сумма:* {good_recs[time][0]["price"]}
*Обоснование:* {choice(good_recs[time][0]["Объяснение"])}""",
                parse_mode=constants.ParseMode.MARKDOWN)
            
            item_json_filename = f"item_json/recom_{good_recs[time][0]['name']}_{time}.json"
            with open(item_json_filename, "w") as fout:
                json.dump(good_recs[time][0], fout)

            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=open(item_json_filename, 'rb')
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Недостаточно данных для прогноза.",
                parse_mode=constants.ParseMode.MARKDOWN)
            
        await ask_choice(update, context)

    elif query.data == "about_company":
        await about_company(update, context)
        await ask_choice(update, context)

    elif query.data == "stats":
        await get_stats(update, context)
        await ask_choice(update, context)

    elif query.data == "applications":
        await get_applications(update, context)
        await ask_choice(update, context)

async def send_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Все товары и услуги", callback_data="forecast_all_goods"),
            ],
            [
                InlineKeyboardButton("Конкретный товар/услуга", callback_data="forecast_specific_good"),
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Выберите:", 
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN)

async def send_full_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE, time=None):
    if user_state.get_state(update) == UserStateEnum.FULL_FORECAST:
        user_state.update_attr(update, "time", time)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='*Товары:*\n\n' + get_paginated_text(0, recom_items_dict[time]), 
            reply_markup=get_navigation_keyboard(0, recom_items_dict[time]),
            parse_mode=constants.ParseMode.MARKDOWN)
    else:
        user_state.update_state(update, UserStateEnum.FULL_FORECAST)

        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("2023 год", callback_data="forecast_all_goods_year"),
                ],
                [
                    InlineKeyboardButton("1 квартал 2023 года", callback_data="forecast_all_goods_q1"),
                ],
                [
                    InlineKeyboardButton("2 квартал 2023 года", callback_data="forecast_all_goods_q2"),
                ],
                [
                    InlineKeyboardButton("3 квартал 2023 года", callback_data="forecast_all_goods_q3"),
                ],
                [
                    InlineKeyboardButton("4 квартал 2023 года", callback_data="forecast_all_goods_q4"),
                ]
            ]
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Выберите период:", 
            reply_markup=reply_markup,
            parse_mode=constants.ParseMode.MARKDOWN)
    
def recom_by_item(item_name: str):
    result = {}
    for time, recoms in recom_dict.items():
        result[time] = list(filter(lambda x: x["name"] == item_name, recoms))

    return result

async def send_specific_forecast(update: Update, context: ContextTypes.DEFAULT_TYPE, good_num: int = None):
    if user_state.get_state(update) == UserStateEnum.GOOD_FORECAST:
        user_state.update_attr(update, "good_num", good_num)
        goods = user_state.get_attr(update, "goods_list")
        good = goods[good_num - 1]

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f'Выбраный товар/услуга: {good}',
            parse_mode=constants.ParseMode.MARKDOWN)
        
        recs = recom_by_item(good)
        user_state.update_attr(update, "good_recs", recs)
        

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("2023 год", callback_data="forecast_specific_good_year"),],
                [InlineKeyboardButton("1 квартал 2023 года", callback_data="forecast_specific_good_q1"),],
                [InlineKeyboardButton("2 квартал 2023 года", callback_data="forecast_specific_good_q2"),],
                [InlineKeyboardButton("3 квартал 2023 года", callback_data="forecast_specific_good_q3"),],
                [InlineKeyboardButton("4 квартал 2023 года", callback_data="forecast_specific_good_q4"),]
            ]
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Выберите период:", 
            reply_markup=reply_markup,
            parse_mode=constants.ParseMode.MARKDOWN)

    else:
        user_state.update_state(update, UserStateEnum.GOOD_FORECAST)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='Введите название товара/услуги:',
            parse_mode=constants.ParseMode.MARKDOWN)

async def find_good(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sim_items = get_top_n_similar_products(update.message.text, kontract_item_names)
    user_state.update_attr(update, "goods_list", sim_items)

    items_text = "\n".join([f"{item_num + 1}. {item}" for item_num, item in enumerate(sim_items)])

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("1", callback_data="good_1"),
                InlineKeyboardButton("2", callback_data="good_2"),
                InlineKeyboardButton("3", callback_data="good_3"),
                InlineKeyboardButton("4", callback_data="good_4"),
                InlineKeyboardButton("5", callback_data="good_5"),
            ],
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Найденные товары:*\n\n" + items_text + "\n\n" + "Выберете товар.\nПримечание: если нужный товар вы не обнаружили, то уточните текстовой запрос.""",
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN
    )

async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_state.get_nickname(update):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=prompts.AUTH_NO
        )
    else:
        status = user_state.get_state(update)
        if status == UserStateEnum.REMAINS:
            await send_remains(update, context)
            await got_to_web_service(update, context)
            await ask_choice(update, context)
        elif status == UserStateEnum.GOOD_FORECAST:
            await find_good(update, context)
        
        else:
            await got_to_web_service(update, context)
            user_state.update_state(update, UserStateEnum.START)
            await ask_choice(update, context)

async def get_applications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = f"""select *
from public.applications a 
join public.user_companies uc on uc.user_id = a.author_id 
join public.user_companies uc1 on uc1.company_id = uc.company_id
where uc1.user_id = '{user_state.get_uuid(update)}'"""
    
    user_q = "select * from users"
    
    applications = db_request(q, settings.db_name_projects)

    if not applications:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Вы еще не создали ни одной заявки.\n Переходите в веб-сервис и создайте свою первую заявку: http://glavcontrol.dev-stand.com !")

    else:
        users = db_request(user_q, settings.db_name_users)
        users_dict = {u[0]: u[1] for u in users}

        applications_texts = []
        for item_row, item in enumerate(applications):
            text = f"*Заявка {item_row + 1}*"

            if item[6]:
                text = text + f"\nКоличество товаров/услуг: {item[6]}"

            if item[12]:
                text = text + f"\nСумма: {item[12]} рублей"

            if item[4] and item[5]:
                text = text + f"\nДата исполнения: {item[4].strftime('%d.%m.%Y')} - {item[5].strftime('%d.%m.%Y')}"

            if item[14]:
                text = text + f"\nАвтор: {users_dict[item[14]]}"

            if item[15]:
                text = text + f"\nСтатус: {'Готово' if item[15] == 'ready' else 'Черновик'}"

            if item[-2]:
                text = text + f"\nДата создания: {item[-2].strftime('%d.%m.%Y')}"

            applications_texts.append(text)

        applications_text = '\n\n'.join(applications_texts)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"*Заявки:*\n\n{applications_text}", 
            parse_mode=constants.ParseMode.MARKDOWN)
