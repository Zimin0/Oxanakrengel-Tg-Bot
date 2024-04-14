from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from config import DEBUG
from json_text_for_bot import load_phrases_from_json_file

def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора типа доставки."""
    SHIPPING_METHODS = load_phrases_from_json_file("SHIPPING_METHODS")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=readable, callback_data=slug)] for slug, readable in SHIPPING_METHODS.items()
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора способа оплаты."""
    PAYMENT_METHODS = load_phrases_from_json_file("PAYMENT_METHODS")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=readable, callback_data='payment:'+slug) for slug, readable in PAYMENT_METHODS.items()]
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_confirmation_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для подтверждение выбора. """
    YES, NO = load_phrases_from_json_file("YES", "NO")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=YES, callback_data="confirm_support_yes")],
        [InlineKeyboardButton(text=NO, callback_data="suport_request")]
    ])
    return keyboard

def get_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру с кнопкой "тех.поддержка" """
    TECH_SUPPORT = load_phrases_from_json_file("TECH_SUPPORT")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TECH_SUPPORT, callback_data="suport_request")],
    ])
    return keyboard

def get_last_product_keyboard(product_name: str) -> InlineKeyboardMarkup:
    """Создает inline-клавиатуру для возвращения к последнему товару."""
    short_product_name = ' '.join(product_name.split()[:4]) + '...'
    BACK_TO_PRODUCT = load_phrases_from_json_file("BACK_TO_PRODUCT")
    callback_data = 'get_product'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{BACK_TO_PRODUCT}"{short_product_name}"', callback_data=callback_data)],
    ])
    return keyboard

def merge_keyboards(*keyboards: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """Объединяет несколько инлайн-клавиатур в одну."""
    all_buttons = []
    for keyboard in keyboards:
        all_buttons.extend(keyboard.inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=all_buttons)

def get_sizes_keyboard(product_info: dict) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с доступными размерами товара."""
    SIZE = load_phrases_from_json_file("SIZE")
    buttons = []
    row = []
    if not product_info['sizes']:
        return None
    for size in product_info['sizes']:
        new_button = InlineKeyboardButton(text=size+SIZE, callback_data=f"size_{size}")
        row.append(new_button)  # Добавляем кнопку в текущий ряд
        if len(row) == 2:  # Проверяем, достиг ли ряд желаемого количества кнопок
            buttons.append(row)  # Добавляем готовый ряд в общий список
            row = []  # Очищаем ряд для следующих кнопок
    if row:  # Добавляем оставшиеся кнопки, если они есть
        buttons.append(row)
    size_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return size_keyboard

def get_pay_keyboard() -> InlineKeyboardMarkup:
    """ Клавиарура "Перейти к оплате." """
    GO_PAY = load_phrases_from_json_file("GO_PAY")
    if DEBUG:
        PAY = f"Сафонов, {GO_PAY}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=GO_PAY, callback_data="payment_request")],
    ])
    return keyboard

def get_final_pay_keyboard(payment_url) -> InlineKeyboardMarkup:
    """ Клавиатура "Оплатить" и "Я оплатил" """
    PAY, CHECK_PAYMENT = load_phrases_from_json_file("PAY", "CHECK_PAYMENT")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=PAY, url=payment_url)],
        [InlineKeyboardButton(text=CHECK_PAYMENT, callback_data="check_payment_request")], 
    ])
    return keyboard
