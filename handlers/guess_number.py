# handlers/guess_number.py
import random
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import guess_number_buttons, main_menu, remove_kb

router = Router()

class GuessNumberGame(StatesGroup):
    number = State()
    attempts = State()

MAX_ATTEMPTS = 7
MAX_NUMBER = 100

@router.message(lambda message: message.text == "🎲 Угадай число")
async def start_guess_number(message: types.Message, state: FSMContext):
    secret_number = random.randint(1, MAX_NUMBER)
    await state.update_data(number=secret_number, attempts=0)
    await state.set_state(GuessNumberGame.number)
    await message.answer(
        f"Я загадал число от 1 до {MAX_NUMBER}. У тебя {MAX_ATTEMPTS} попыток!\n"
        "Введи число:",
        reply_markup=remove_kb
    )

@router.message(GuessNumberGame.number)
async def guess_number(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)
        return

    if message.text == "🔄 Новая игра":
        return await start_guess_number(message, state)

    if not message.text.isdigit():
        await message.answer(
            "Пожалуйста, введи целое число от 1 до 100.",
            reply_markup=remove_kb
        )
        return

    # Преобразуем в число
    guess = int(message.text)

    if guess < 1 or guess > MAX_NUMBER:
        await message.answer(
            f"Число должно быть от 1 до {MAX_NUMBER}.",
            reply_markup=remove_kb
        )
        return

    user_data = await state.get_data()
    secret = user_data["number"]
    attempts = user_data.get("attempts", 0)

    attempts += 1
    await state.update_data(attempts=attempts)

    if guess == secret:
        await message.answer(
            f"🎉 Поздравляю! Ты угадал число {secret} за {attempts} попыток!",
            reply_markup=main_menu
        )
        await state.clear()
    elif attempts >= MAX_ATTEMPTS:
        await message.answer(
            f"💀 Попытки закончились. Загаданное число было: {secret}",
            reply_markup=main_menu
        )
        await state.clear()
    else:
        hint = "больше" if guess < secret else "меньше"
        remaining = MAX_ATTEMPTS - attempts
        await message.answer(
            f"Неверно! Загаданное число {hint}. Осталось попыток: {remaining}",
            reply_markup=remove_kb
        )