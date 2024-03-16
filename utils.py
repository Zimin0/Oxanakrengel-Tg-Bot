from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.types import Message

def is_size_callback(callback_query: types.CallbackQuery) -> bool:
    """ Определяет, что пользователь нажал на кнопку размера. """
    if callback_query.data:
        return callback_query.data.startswith('size_')
    return False

def is_payment_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором способа оплаты."""
    return callback_query.data.startswith('payment_')

def get_args_from_message(message: Message) -> str:
    """ Достает аргументы, переданные в ссылке в параметре ?start=... """
    parts = message.text.split(maxsplit=1)
    args = None
    if len(parts) > 1:
        args = parts[1]
    return args

def get_product_content(product_info: dict) -> list[list, list, InlineKeyboardMarkup]:
    """ Форматирует и возвращает текстовое сообщение с информацией о товаре и клавиатуру """
    message_text = [
        f"<b>{product_info['title']}</b>\n"
        f"Цена: <i>{product_info['price'].lower()}</i>\n"
        f"Доступные размеры: {', '.join([f'<b>{size}</b>' for size in product_info['sizes']])}\n"
        f"<a href='{product_info['url']}'>Подробнее о товаре</a>\n\n"
        f"{product_info['description']}"
    ]
    size_keyboard = get_sizes_keyboard(product_info)
    photoes = get_product_photoes(product_info)

    return message_text, photoes, size_keyboard


def get_product_photoes(product_info: dict) -> list:
    """ Возвращает фотографии товара с сайта. """
    media = []
    for url in product_info['image_urls']:
        media.append(types.InputMediaPhoto(media=url))
    return media

def get_sizes_keyboard(product_info: dict) -> InlineKeyboardMarkup:
    """ Возвращает клавиатуру с доступными размерами товара. """
    buttons = []
    if not product_info['sizes']:
        return None
    for size in product_info['sizes']:
        new_button = [InlineKeyboardButton(text=size, callback_data=f"size_{size}")] # Создание кнопок для каждого размера
        buttons.append(new_button) 
    size_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) # Создание инлайн-клавиатуры с этими кнопками
    return size_keyboard