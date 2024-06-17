from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from src import handlers
from settings import settings


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.bot_token).build()

    start_handler = CommandHandler("start", handlers.start)
    application.add_handler(start_handler)
    remains_handler = CommandHandler("remains", handlers.send_remains)
    application.add_handler(remains_handler)
    forecast_handler = CommandHandler("forecast", handlers.send_forecast)
    application.add_handler(forecast_handler)
    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), handlers.text_msg
    )
    application.add_handler(text_handler)
    application.add_handler(CallbackQueryHandler(handlers.button_callback))

    print("Start")
    application.run_polling()
