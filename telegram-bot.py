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
import json
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_links import get_bot_link_with_arg, get_product_link_in_shop
from bs_parser import WebPageParser

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
parser = WebPageParser(debug=True, folder='products_json')


class OrderClothes(StatesGroup):
    show_clothes = State()
    choose_size = State()
    choose_payment_method = State()
    get_personal_data = State()
    send_request_to_support = State()


def get_args_from_message(message: Message) -> str:
    """ Достает аргументы, переданные в ссылке в параметре ?start=... """
    parts = message.text.split(maxsplit=1)
    args = None
    if len(parts) > 1:
        args = parts[1]
    return args


from aiogram import Bot, types

async def send_product_info(message: Message, product_info: dict):
    # Форматирование и отправка текстового сообщения с информацией о товаре
    message_text = (
        f"<b>{product_info['title']}</b>\n"
        f"Цена: <i>{product_info['price']}</i>\n"
        f"Доступные размеры: {', '.join(product_info['sizes'])}\n"
        f"<a href='{product_info['url']}'>Подробнее о товаре</a>\n\n"
        f"{product_info['description']}"
    )
    # Создание группы фотографий товара
    media = [types.InputMediaPhoto(media=url) for url in product_info['image_urls']]
    # Отправка изображений как альбома, если есть изображения
    if media:
        await message.answer_media_group(media)

    await message.answer(message_text, parse_mode='HTML')
    



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """ Этот обработчик получает сообщения с командой /start """

    await state.set_state(OrderClothes.show_clothes)
    await message.answer(hbold("Ищу ваш товар в каталоге..."))
    # await message.answer_sticker(sticker="CAACAgIAAxkBAAEqKnll73MY6EKjiWdKkbwyWuIUapEGlgAC_hEAAo6E8Eup_sGzXXLhQDQE")

    product_name = get_args_from_message(message)
    link_in_shop = get_product_link_in_shop(product_name)
    filename, product_json_str = parser.run(link_in_shop, save_to_file=True)  # Получаем JSON в виде строки
    product_json = json.loads(product_json_str)  # Преобразуем строку в словарь
    await send_product_info(message, product_json)

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