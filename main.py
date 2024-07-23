import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import bot_settings
from handlers import router

async def main():

    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(bot_settings.BOT_API)

    dp = Dispatcher()

    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
