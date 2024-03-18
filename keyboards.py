from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from config import PAYMENT_METHODS

def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора типа доставки."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доставка курьером по Москве🚚", callback_data="delivery_moscow")],
        [InlineKeyboardButton(text="Доставка курьером по России🛫", callback_data="delivery_russia")],
        [InlineKeyboardButton(text="Самовывоз🏃🏼", callback_data="delivery_pickup")],
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора способа оплаты."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=readable, callback_data='payment:'+slug) for slug, readable in PAYMENT_METHODS.items()]
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_confirmation_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для подтверждение выбора. """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да✅", callback_data="confirm_support_yes")],
        [InlineKeyboardButton(text='Нет❌', callback_data="suport_request")]
    ])
    return keyboard

def get_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру с кнопкой "тех.поддержка" """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Тех. поддержка⚙️", callback_data="suport_request")],
    ])
    return keyboard

def get_last_product_keyboard(product_name: str) -> InlineKeyboardMarkup:
    """Создает inline-клавиатуру для возвращения к последнему товару."""
    short_product_name = ' '.join(product_name.split()[:4]) + '...'
    callback_data = 'get_product'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Вернуться к товару ➡️"{short_product_name}"', callback_data=callback_data)],
    ])
    return keyboard

def merge_keyboards(*keyboards: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """Объединяет несколько инлайн-клавиатур в одну."""
    all_buttons = []
    for keyboard in keyboards:
        all_buttons.extend(keyboard.inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=all_buttons)

def get_sizes_keyboard(product_info: dict) -> InlineKeyboardMarkup:
    """ Возвращает клавиатуру с доступными размерами товара. """
    buttons = []
    if not product_info['sizes']:
        return None
    for size in product_info['sizes']:
        new_button = [InlineKeyboardButton(text=size+'-й 🟢', callback_data=f"size_{size}")] # Создание кнопок для каждого размера
        buttons.append(new_button) 
    size_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) # Создание инлайн-клавиатуры с этими кнопками
    return size_keyboard