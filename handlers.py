from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.error import TimedOut, BadRequest

from utils import get_weather, get_cat_url, get_exchange_rate

async def request_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    "Отправить координаты 📍",
                    request_location=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Пожалуйста, поделитесь своей геолокацией:",
        reply_markup=location_keyboard
    )



async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        location = update.message.location

        if location is None:
            latitude = 55.7558
            longitude = 37.6173
        else:
            latitude = location.latitude
            longitude = location.longitude

        context.user_data['location'] = (latitude, longitude)

        weather_report = await get_weather(latitude, longitude)

        await update.message.reply_text(weather_report)

        main_menu = ReplyKeyboardMarkup(
            [
                ["Привет 👋", "Мой ID 🆔"],
                ["Помощь ℹ️", "Фото 🖼️"],
                ["Фото котика 🐕", "Информация 🖥"],
                ["Погода сегодня 🎲"]
            ],
            resize_keyboard=True
        )

        await update.message.reply_text(
            "👌",
            reply_markup=main_menu
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ Не удалось обработать геолокацию."
        )



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Привет 👋", "Мой ID 🆔"],
        ["Помощь ℹ️", "Фото 🖼️"],
        ["Фото котика 🐕", "Информация 🖥"],
        ["Погода сегодня 🎲"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Привет, я бот Влада Беломестнова из группы БСБО-12-23!\n\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )



async def mi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        f"Твой chat_id: {chat_id}"
    )



async def say_hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username

    if username:
        name = f"{username}"
    else:
        name = update.effective_user.first_name

    await update.message.reply_text(
        f"Привет, {name}! Ты написал обычное сообщение!"
    )
    


async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name}\n"
        f"Username: @{user.username}\n"
        f"Chat ID: {update.effective_chat.id}"
    )



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Привет 👋":
        username = update.effective_user.username

        if username:
            name = f"@{username}"
        else:
            name = update.effective_user.first_name

        await update.message.reply_text(
            f"Привет, {username}! 👋"
        )

    elif text == "Мой ID 🆔":
        chat_id = update.effective_chat.id

        await update.message.reply_text(
            f"Твой chat_id: {chat_id}"
        )

    elif text == "Фото 🖼️":
            await send_photo(update, context)
    
    elif text == "Информация 🖥":
        await update.message.reply_text(
        "Функцию получения IP добавим потом. Сейчас показываю курс доллара 💱"
        )
        rate = await get_exchange_rate()
        await update.message.reply_text(rate)
    
    elif text == 'Фото котика 🐕':
            await send_cat_photo(update, context)
    
    elif text == 'Погода сегодня 🎲':
            await request_location(update, context)
        
    elif text == "Помощь ℹ️":
        await update.message.reply_text(
            "Я умею:\n"
            "👋 приветствовать тебя\n"
            "🆔 показывать твой chat_id\n"
            "ℹ️ показывать эту помощь\n"
            "🖼️ показывать твой аватар\n"
            "🐕 показывать фото котика\n"
            "🖥 скоро научусь показывать твой IP\n"
            "🎲 скоро научусь отправлять рандомное число"


        )



async def send_cat_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cat_url = await get_cat_url()

        if not cat_url:
            await update.message.reply_text(
                "😿 Не удалось получить фотографию котика."
            )
            return

        await update.message.reply_photo(
            photo=cat_url
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ Не удалось отправить фотографию котика."
        )



async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        username = user.username or "user"

        timestamp = int(update.message.date.timestamp())

        
        ava_str = f"{timestamp}_{username}"

        
        ava_url = f"https://robohash.org/{ava_str}?set=set1"

        await update.message.reply_photo(
            photo=ava_url
        )

    except TimedOut:
        await update.message.reply_text(
            "⏳ Не удалось получить аватар вовремя. Попробуй ещё раз."
        )

    except BadRequest:
        await update.message.reply_text(
            "❌ Не удалось загрузить аватар."
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ Произошла непредвиденная ошибка при отправке аватара."
        )
