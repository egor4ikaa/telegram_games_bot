from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.reply import main_menu, remove_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! 👋\nВыбери игру:",
        reply_markup=main_menu
    )

@router.message(Command("help"))
@router.message(lambda message: message.text == "❓ Помощь")
async def cmd_help(message: types.Message, state: FSMContext):
    await state.clear()
    help_text = (
        "🎲 <b>Угадай число</b>:\n"
        "Я загадываю число от 1 до 100. Попробуй угадать! У тебя 7 попыток.\n\n"
        "🪨✂️📄 <b>Камень, ножницы, бумага</b>:\n"
        "Выбери один из вариантов. Бот тоже сделает выбор. Победитель определяется по классическим правилам.\n\n"
        "Используй кнопки ниже, чтобы начать игру!"
    )
    await message.answer(help_text, parse_mode="HTML", reply_markup=main_menu)

@router.message(Command("cancel"))
@router.message(lambda message: message.text == "🔙 Назад")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Операция отменена. Возврат в главное меню.",
        reply_markup=main_menu
    )

@router.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        if message.text not in ["🎲 Угадай число", "🪨✂️📄 Камень-ножницы-бумага", "❓ Помощь"]:
            await message.answer(
                "Пожалуйста, используйте кнопки меню для выбора игры.",
                reply_markup=main_menu
            )