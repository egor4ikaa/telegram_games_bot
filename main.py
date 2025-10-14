import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем роутеры
from handlers.common import router as common_router
from handlers.game_handlers import router as game_router

async def main():
    logging.basicConfig(level=logging.INFO)

    # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ТОКЕН БОТА
    bot = Bot(token="7953062934:AAGA7OpKpYC9widr49UVIbc03OtjrOuqOqE")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры
    dp.include_router(game_router)
    dp.include_router(common_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())