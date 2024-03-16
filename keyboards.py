from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора типа доставки."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доставка курьером по России", callback_data="delivery_courier_russia")],
        [InlineKeyboardButton(text="Самовывоз", callback_data="delivery_pickup")],
        [InlineKeyboardButton(text="Доставка курьером по Москве", callback_data="delivery_courier_moscow")]
    ])
    return keyboard

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Возвращает инлайн-клавиатуру для выбора способа оплаты."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Карта РФ', callback_data='payment_card')],
        [InlineKeyboardButton(text='Paypal', callback_data='payment_paypal')]
    ])
    return keyboard