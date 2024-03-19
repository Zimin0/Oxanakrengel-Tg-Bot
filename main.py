import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import sys
import logging
from handlers.product_choice_handlers import product_choice_router
from handlers.personal_data_handlers import personal_data_router
from handlers.support_handlers import support_router
from handlers.payment_handlers import payment_router

from config import TOKEN

async def main() -> None:
    dp = Dispatcher() # Слушает входящие уведомления Telegram и передает их в handlers
    dp.include_router(product_choice_router)
    dp.include_router(personal_data_router)
    dp.include_router(support_router)
    dp.include_router(payment_router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())