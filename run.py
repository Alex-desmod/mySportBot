import asyncio
import os
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers_common import router

async def main():
    load_dotenv()
    TOKEN = os.getenv('BOT_TOKEN')

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="[%(asctime)s.%(msecs)03d] %(module)s %(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('The bot is off')