import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from handlers import (
    start,
    mi_id,
    user_info,
    button_handler,
    say_hi,
    handle_location
)

def run_bot():
    load_dotenv()

    token = os.getenv("TOKEN")
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(
        CommandHandler("start", start)
    )
    
    application.add_handler(
        CommandHandler("miID", mi_id)
    )
    
    application.add_handler(
        CommandHandler("info", user_info)
    )
    
    application.add_handler(
    MessageHandler(filters.TEXT, button_handler)
    )
    application.add_handler(
    MessageHandler(filters.TEXT, say_hi)
    )
    application.add_handler(
    MessageHandler(filters.LOCATION, handle_location)
    )

    application.run_polling(poll_interval=20.0)