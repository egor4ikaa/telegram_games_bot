# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import common, rps, guess_number

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(common.router)
    dp.include_router(rps.router)
    dp.include_router(guess_number.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())