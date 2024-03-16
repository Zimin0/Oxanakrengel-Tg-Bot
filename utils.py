from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.types import Message

import re

def is_size_callback(callback_query: types.CallbackQuery) -> bool:
    """ Определяет, что пользователь нажал на кнопку размера. """
    if callback_query.data:
        return callback_query.data.startswith('size_')
    return False

def is_payment_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором способа оплаты."""
    return callback_query.data.startswith('payment_')

def is_delivery_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором типа доставки."""
    return callback_query.data.startswith("delivery_")

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
    message_text = "\n".join(message_text)

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

class Validators:
    """ Валидаторы для личных данных пользователя. """
    @staticmethod
    def validate_name(name):
        """Проверка имени на корректность."""
        if not re.match(r'^[A-Za-zА-Яа-я ]+$', name):
            raise ValueError("Имя должно содержать только буквы и пробелы.")

    @staticmethod
    def validate_email(email):
        """Проверка email с помощью регулярного выражения."""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Некорректный формат электронной почты.")

    @staticmethod
    def validate_phone_number(phone_number):
        """Проверка телефонного номера."""
        if not re.match(r'^\+?[1-9]\d{10,14}$', phone_number):
            raise ValueError("Некорректный формат номера телефона.")

    @staticmethod
    def validate_address(delivery_address):
        """Простая проверка адреса доставки на непустоту."""
        if not delivery_address or not delivery_address.strip():
            raise ValueError("Адрес доставки не может быть пустым.")