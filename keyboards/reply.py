# keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Камень, ножницы, бумага")],
        [KeyboardButton(text="🎲 Угадай число")],
        [KeyboardButton(text="❓ Помощь")]
    ],
    resize_keyboard=True
)

# Кнопки для КНБ
rps_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪨 Камень"), KeyboardButton(text="✂️ Ножницы"), KeyboardButton(text="📄 Бумага")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

# Кнопки для угадай числа
guess_number_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Новая игра"), KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)


remove_kb = ReplyKeyboardRemove()