from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import random
import states.game_states as game_states
from keyboards.reply import main_menu, rps_menu, rps_after_game_menu, remove_keyboard

router = Router()

# ===== УГАДАЙ ЧИСЛО =====
@router.message(lambda message: message.text == "🎲 Угадай число")
async def start_guess_number(message: types.Message, state: FSMContext):
    await state.set_state(game_states.GuessNumberGame.guessing)
    secret_number = random.randint(1, 100)
    await state.update_data(
        secret_number=secret_number,
        attempts=7
    )
    await message.answer(
        f"🎯 Я загадал число от 1 до 100!\n"
        f"У тебя 7 попыток. Попробуй угадать!\n\n"
        f"Просто напиши число в чат:",
        reply_markup=main_menu
    )

@router.message(StateFilter(game_states.GuessNumberGame.guessing))
async def process_guess(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Пожалуйста, введите число от 1 до 100!")
        return

    user_guess = int(message.text)
    data = await state.get_data()
    secret_number = data['secret_number']
    attempts = data['attempts'] - 1

    if user_guess < 1 or user_guess > 100:
        await message.answer("❌ Число должно быть от 1 до 100!")
        return

    if user_guess == secret_number:
        await message.answer(
            f"🎉 Поздравляю! Ты угадал число {secret_number}!",
            reply_markup=main_menu
        )
        await state.clear()
        return

    if attempts == 0:
        await message.answer(
            f"❌ Попытки закончились! Я загадал число {secret_number}.",
            reply_markup=main_menu
        )
        await state.clear()
        return

    # Даем подсказку
    hint = "Загаданное число МЕНЬШЕ" if user_guess > secret_number else "Загаданное число БОЛЬШЕ"
    await state.update_data(attempts=attempts)
    await message.answer(
        f"{hint}\n"
        f"❌ Не угадал! Осталось попыток: {attempts}\n"
        f"Попробуй еще раз:"
    )

# ===== КАМЕНЬ-НОЖНИЦЫ-БУМАГА =====
@router.message(lambda message: message.text == "🪨✂️📄 Камень-ножницы-бумага")
async def start_rps(message: types.Message, state: FSMContext):
    await state.set_state(game_states.RPSGame.choosing)
    await message.answer(
        "🎮 Выбери свой вариант:",
        reply_markup=rps_menu
    )

@router.message(StateFilter(game_states.RPSGame.choosing))
async def process_rps_choice(message: types.Message, state: FSMContext):
    # Обработка кнопки "Назад"
    if message.text == "🔙 Назад":
        await state.clear()
        await message.answer(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu
        )
        return

    user_choice = message.text.lower()
    bot_choice = random.choice(["камень", "ножницы", "бумага"])

    # Определяем выбор пользователя по кнопкам
    if "камень" in user_choice or "🪨" in user_choice:
        user_choice_clean = "камень"
    elif "ножницы" in user_choice or "✂️" in user_choice:
        user_choice_clean = "ножницы"
    elif "бумага" in user_choice or "📄" in user_choice:
        user_choice_clean = "бумага"
    else:
        await message.answer(
            "❌ Пожалуйста, выбери вариант с помощью кнопок ниже:",
            reply_markup=rps_menu
        )
        return

    # Определяем победителя
    if user_choice_clean == bot_choice:
        result = "🤝 Ничья!"
    elif (user_choice_clean == "камень" and bot_choice == "ножницы") or \
         (user_choice_clean == "ножницы" and bot_choice == "бумага") or \
         (user_choice_clean == "бумага" and bot_choice == "камень"):
        result = "🎉 Ты победил!"
    else:
        result = "❌ Бот победил!"

    # Эмодзи для выбора
    emoji_map = {"камень": "🪨", "ножницы": "✂️", "бумага": "📄"}

    await message.answer(
        f"Твой выбор: {emoji_map[user_choice_clean]} {user_choice_clean}\n"
        f"Выбор бота: {emoji_map[bot_choice]} {bot_choice}\n\n"
        f"{result}",
        reply_markup=remove_keyboard  # Скрываем клавиатуру после выбора
    )

    # Предлагаем сыграть еще
    await message.answer(
        "Хочешь сыграть еще раз?",
        reply_markup=rps_after_game_menu
    )
    # Не очищаем состояние, чтобы обработать выбор "Сыграть еще"

# Обработка выбора после игры
@router.message(StateFilter(game_states.RPSGame.choosing))
async def handle_after_game_choice(message: types.Message, state: FSMContext):
    if message.text == "🔄 Сыграть еще":
        # Начинаем новую игру
        await message.answer(
            "🎮 Отлично! Выбери свой вариант:",
            reply_markup=rps_menu
        )
        # Состояние остается тем же (choosing)

    elif message.text == "🔙 Назад":
        await state.clear()
        await message.answer(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu
        )
    else:
        await message.answer(
            "Пожалуйста, выбери один из вариантов:",
            reply_markup=rps_after_game_menu
        )