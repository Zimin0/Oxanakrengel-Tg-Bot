import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import sys
import logging
from handlers import router
from config import TOKEN

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher() # Слушает входящие уведомления Telegram и передает их в 
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())