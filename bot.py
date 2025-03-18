import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.main_handler import main_router
from handlers.admin_handler import admin_router

bot = Bot(token='token')

dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(main_router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("By by, homie")