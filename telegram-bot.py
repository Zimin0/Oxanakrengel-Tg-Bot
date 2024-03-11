import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from create_links import get_bot_link_with_arg, get_product_link_in_shop
from bs_parser import WebPageParser

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
parser = WebPageParser(debug=True)

def get_args_from_message(message: Message) -> str:
    """ Достает аргументы, переданные в ссылке в параметре ?start=... """
    parts = message.text.split(maxsplit=1)
    args = None
    if len(parts) > 1:
        args = parts[1]
    return args


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """ Этот обработчик получает сообщения с командой /start """
    product_name = get_args_from_message(message)
    link_in_shop = get_product_link_in_shop(product_name)
    product_json = parser.run(link_in_shop)
    await message.answer(f"Информация о товаре {hbold(product_name)}: {product_json}")
    
    # await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Этот обработчик будет пересылать полученное сообщение обратно отправителю
    По умолчанию обработчик сообщений будет обрабатывать все типы сообщений (текст, фото, стикеры и т.д.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())