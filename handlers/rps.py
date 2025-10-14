# handlers/rps.py
import random
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import rps_buttons, main_menu, remove_kb

router = Router()

class RPSGame(StatesGroup):
    playing = State()

choices = ["🪨 Камень", "✂️ Ножницы", "📄 Бумага"]
bot_choices = ["🪨", "✂️", "📄"]

@router.message(lambda message: message.text == "🎮 Камень, ножницы, бумага")
async def start_rps(message: types.Message, state: FSMContext):
    await state.set_state(RPSGame.playing)
    await message.answer("Выбери свой ход:", reply_markup=rps_buttons)

@router.message(RPSGame.playing)
async def play_rps(message: types.Message, state: FSMContext):
    user_choice = message.text
    if user_choice == "🔙 Назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)
        return

    if user_choice not in choices:
        await message.answer("Пожалуйста, используй кнопки.", reply_markup=rps_buttons)
        return

    bot_choice = random.choice(bot_choices)
    user_index = choices.index(user_choice)
    bot_index = bot_choices.index(bot_choice)

    # Преобразуем в числа для сравнения: 0 - камень, 1 - ножницы, 2 - бумага
    if user_index == bot_index:
        result = "🤝 Ничья!"
    elif (user_index - bot_index) % 3 == 1:
        result = "🤖 Бот победил!"
    else:
        result = "🎉 Ты победил!"

    # Отправляем результат и **скрываем клавиатуру**
    await message.answer(
        f"Твой выбор: {user_choice}\n"
        f"Выбор бота: {bot_choice}\n\n"
        f"{result}",
        reply_markup=remove_kb  # ← скрываем клавиатуру
    )



    # Предлагаем сыграть снова
    await message.answer("Хочешь сыграть ещё?", reply_markup=rps_buttons)