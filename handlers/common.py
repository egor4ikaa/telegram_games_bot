# handlers/common.py
from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! 👋\nВыбери игру:",
        reply_markup=main_menu
    )



@router.message(Command("help"))
@router.message(lambda message: message.text == "❓ Помощь")
async def cmd_help(message: types.Message):
    help_text = (
        "🎲 <b>Угадай число</b>:\n"
        "Я загадываю число от 1 до 100. Попробуй угадать! У тебя 7 попыток.\n\n"
        "🪨✂️📄 <b>Камень, ножницы, бумага</b>:\n"
        "Выбери один из вариантов. Бот тоже сделает выбор. Победитель определяется по классическим правилам.\n\n"
        "Используй кнопки ниже, чтобы начать игру!"
    )
    await message.answer(help_text, parse_mode="HTML", reply_markup=main_menu)
