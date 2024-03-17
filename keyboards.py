from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора типа доставки."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доставка курьером по России", callback_data="delivery_russia")],
        [InlineKeyboardButton(text="Самовывоз", callback_data="delivery_pickup")],
        [InlineKeyboardButton(text="Доставка курьером по Москве", callback_data="delivery_moscow")]
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора способа оплаты."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Карта РФ', callback_data='payment_card')],
        [InlineKeyboardButton(text='Paypal', callback_data='payment_paypal')]
    ])
    return merge_keyboards(keyboard, get_support_keyboard())

def get_confirmation_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для подтверждение выбора. """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="confirm_support_yes")],
        [InlineKeyboardButton(text='Нет', callback_data="suport_request")]
    ])
    return keyboard

def get_support_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру с кнопкой "тех.поддержка" """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Тех. поддержка", callback_data="suport_request")],
    ])
    return keyboard

def get_last_product_keyboard(product_name: str) -> InlineKeyboardMarkup:
    """Создает inline-клавиатуру для возвращения к последнему товару."""
    short_product_name = ' '.join(product_name.split()[:4]) + '...'
    callback_data = 'get_product'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Вернуться к товару "{short_product_name}"', callback_data=callback_data)],
    ])
    return keyboard

def merge_keyboards(*keyboards: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """Объединяет несколько инлайн-клавиатур в одну."""
    all_buttons = []
    for keyboard in keyboards:
        all_buttons.extend(keyboard.inline_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=all_buttons)
