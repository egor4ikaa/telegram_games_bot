from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Угадай число"), KeyboardButton(text="🪨✂️📄 Камень-ножницы-бумага")],
        [KeyboardButton(text="📖 Читать сайт"), KeyboardButton(text="❓ Помощь")]
    ],
    resize_keyboard=True
)

# Меню для игры в камень-ножницы-бумагу
rps_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪨 Камень"), KeyboardButton(text="✂️ Ножницы")],
        [KeyboardButton(text="📄 Бумага"), KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
# В reply.py добавьте:

# Клавиатура для чтения сайта
reading_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➡️ Далее")],
        [KeyboardButton(text="🔖 Поставить закладку"), KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# Меню после игры (сыграть еще или выйти)
rps_after_game_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Сыграть еще"), KeyboardButton(text="🔙 В главное меню")]
    ],
    resize_keyboard=True
)

# Для скрытия клавиатуры
remove_keyboard = ReplyKeyboardRemove()