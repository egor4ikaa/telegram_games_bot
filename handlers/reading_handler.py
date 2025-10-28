# handlers/reading_handler.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.reading_states import ReadingWebsite
from keyboards.reply import reading_menu, main_menu

# Пример "сайта" — список абзацев
WEBSITE_CONTENT = [
    "Добро пожаловать на наш сайт! 🌐\nЭто первый абзац.",
    "Здесь вы узнаете много интересного о технологиях и ботах.",
    "AI и Telegram — отличное сочетание для автоматизации.",
    "Не забывайте ставить закладки, чтобы не потерять прогресс!",
    "Спасибо, что читаете! 💡"
]

router = Router()

@router.message(lambda message: message.text == "📖 Читать сайт")
async def start_reading(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("reading_position", 0)

    if current_index >= len(WEBSITE_CONTENT):
        await message.answer("Вы уже прочитали весь сайт! 🎉", reply_markup=main_menu)
        await state.clear()
        return

    # Напоминаем, если есть сохранённая позиция
    if current_index > 0:
        await message.answer(
            f"📌 Вы остановились здесь. Продолжаем чтение:",
            reply_markup=reading_menu
        )
    else:
        await message.answer("Начинаем чтение сайта:", reply_markup=reading_menu)

    await message.answer(WEBSITE_CONTENT[current_index])
    await state.update_data(reading_position=current_index)
    await state.set_state(ReadingWebsite.reading)


@router.message(StateFilter(ReadingWebsite.reading))
async def handle_reading_actions(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("reading_position", 0)

    if message.text == "➡️ Далее":
        next_index = current_index + 1
        if next_index >= len(WEBSITE_CONTENT):
            await message.answer("📖 Вы дочитали до конца! Спасибо за внимание.", reply_markup=main_menu)
            await state.clear()
        else:
            await message.answer(WEBSITE_CONTENT[next_index])
            await state.update_data(reading_position=next_index)
            await state.set_state(ReadingWebsite.reading)

    elif message.text == "🔖 Поставить закладку":
        # Закладка уже сохраняется автоматически при каждом переходе,
        # но можно явно подтвердить
        await message.answer(
            f"🔖 Закладка сохранена на позиции {current_index + 1} из {len(WEBSITE_CONTENT)}.",
            reply_markup=reading_menu
        )

    elif message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Возвращаемся в главное меню:", reply_markup=main_menu)

    else:
        # Некорректный ввод
        await message.answer("Пожалуйста, используйте кнопки:", reply_markup=reading_menu)