from aiogram.types import InlineKeyboardMarkup
from aiogram import types
from aiogram.types import Message

import config

from keyboards import get_sizes_keyboard
import re
from json_text_for_bot import load_phrases_from_json_file

def is_size_callback(callback_query: types.CallbackQuery) -> bool:
    """ Определяет, что пользователь нажал на кнопку размера. """
    if callback_query.data:
        return callback_query.data.startswith('size_')
    return False

def is_payment_choice_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором способа оплаты."""
    return callback_query.data.startswith('payment:')

def is_delivery_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором типа доставки."""
    return callback_query.data.startswith("delivery_")

def is_support_callback(callback_query: types.CallbackQuery) -> bool:
    """ Проверяет, является ли callback_query нажатием кнопки "техподдержка". """
    return callback_query.data.startswith('suport_request')

def is_support_message_confirmation_callback(callback_query: types.CallbackQuery) -> bool:
    """ Проверяет, является ли callback_query нажатием кнопки "да" во время запроса в техподдержку. """
    return callback_query.data.startswith('confirm_support_yes')

def is_payment_callback(callback_query: types.CallbackQuery) -> bool:
    """ Проверяет, является ли callback_query нажатием кнопки "оплатить". """
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
    AVAILABLE_SIZES, ABOUT_PRODUCT, PRICE_PRODUCT, PRE_PRODUCT_SYMBOL, POST_PRODUCT_SYMBOL = load_phrases_from_json_file(
        "AVAILABLE_SIZES",
        "ABOUT_PRODUCT",
        "PRICE_PRODUCT",
        "PRE_PRODUCT_SYMBOL",
        "POST_PRODUCT_SYMBOL"
        )
    message_text = [
        f"{PRE_PRODUCT_SYMBOL} <b>{product_info['title']}</b> {POST_PRODUCT_SYMBOL} \n\n"
        f"{PRICE_PRODUCT}: <i>{product_info['price'].lower()}</i>\n"
        f"{AVAILABLE_SIZES}: {', '.join([f'<b>{size}</b>' for size in product_info['sizes']])}\n"
        f"\n<a href='{product_info['url']}'>{ABOUT_PRODUCT}</a>\n\n"
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

def if_debug(func):
    """Декоратор, отключающий валидацию в режиме отладки."""
    def wrapper(*args, **kwargs):
        if config.DEBUG:
            return
        else:
            return func(*args, **kwargs)
    return wrapper

def parse_price_and_valute(price_str:str):
    """ Парсит строку формата 123.22 рублей """
    # valutes = ('ruble', 'dollar', 'euro')
    print(f"{price_str=}")
    result = price_str.strip().lower().split()
    if len(result) == 2:
        price, valute = result
        if valute[:3] in ('руб', 'р'):
            valute = 'ruble' 
            return float(price), valute
        else:
            raise ValueError(f"Неизвестная валюта: {result}")
    else:
        raise ValueError(f"Не знаю, как распарсить цену: {result}")

class Validators:
    """ Валидаторы для личных данных пользователя. """

    @if_debug
    @staticmethod
    def validate_name(name):
        """Проверка имени на корректность."""
        if not re.match(r'^[A-Za-zА-Яа-я ]+$', name):
            raise ValueError("Имя должно содержать только буквы и пробелы.")

    @if_debug
    @staticmethod
    def validate_email(email):
        """Проверка email с помощью регулярного выражения."""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Некорректный формат электронной почты.")

    @if_debug
    @staticmethod
    def validate_phone_number(phone_number):
        """Проверка телефонного номера."""
        if not re.match(r'^\+?[1-9]\d{10,14}$', phone_number):
            raise ValueError("Некорректный формат номера телефона.")

    @if_debug
    @staticmethod
    def validate_address(delivery_address):
        """Простая проверка адреса доставки на непустоту."""
        if not delivery_address or not delivery_address.strip() or len(delivery_address) < 20:
            raise ValueError("Это не похоже на адрес.")
    
    @if_debug
    @staticmethod
    def validate_support_message(message):
        """ Валидация сообщения в поддержку """
        message = message.strip()
        if len(message.split()) < 10 or len(message) < 40:
            raise ValueError("Запрос в поддержку должен содержать минимум 10 слов и 40 символов.")
        
