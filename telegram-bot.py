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
from aiogram import Bot, types

from create_links import get_bot_link_with_arg, get_product_link_in_shop
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs_parser import WebPageParser
# from aiogram.dispatcher.filters import StateFilter


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()

router = Router()
dp.include_router(router)
parser = WebPageParser(debug=True, folder='products_json')


class OrderClothes(StatesGroup):
    show_clothes = State()
    choose_size = State()
    choose_payment_method = State()
    get_personal_data = State()
    choose_delivery_method = State() 
    send_request_to_support = State()

class PersonalDataForm(StatesGroup):
    wait_for_name = State()
    wait_for_surname = State()
    wait_for_email = State()
    wait_for_phone_number = State()
    wait_for_delivery_address = State()


def get_args_from_message(message: Message) -> str:
    """ Достает аргументы, переданные в ссылке в параметре ?start=... """
    parts = message.text.split(maxsplit=1)
    args = None
    if len(parts) > 1:
        args = parts[1]
    return args

def is_size_callback(callback_query: types.CallbackQuery) -> bool:
    """ Определяет, что пользователь нажал на кнопку размера. """
    if callback_query.data:
        return callback_query.data.startswith('size_')
    return False

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

async def send_product_info(message: Message, product_info: dict):
    """ Форматирует и отправляет текстовое сообщение с информацией о товаре """
    message_text = (
        f"<b>{product_info['title']}</b>\n"
        f"Цена: <i>{product_info['price']}</i>\n"
        f"Доступные размеры: {', '.join(product_info['sizes'])}\n"
        f"<a href='{product_info['url']}'>Подробнее о товаре</a>\n\n"
        f"{product_info['description']}"
    )
    
    buttons = []
    for size in product_info['sizes']:
        new_button = [InlineKeyboardButton(text=size, callback_data=f"size_{size}")] # Создание кнопок для каждого размера
        buttons.append(new_button) 

    size_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) # Создание инлайн-клавиатуры с этими кнопками
    
    media = []
    for url in product_info['image_urls']:
        media.append(types.InputMediaPhoto(media=url))
    if media:
        await message.answer_media_group(media) # Отправка медиа в виде альбома
    
    await message.answer(message_text, parse_mode='HTML', reply_markup=size_keyboard) # Отправка текстового сообщения с инлайн-клавиатурой


def is_payment_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором способа оплаты."""
    return callback_query.data.startswith('payment_')

##################### Обработчики #####################
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """ Этот обработчик получает сообщения с командой /start """
    await state.clear() 
    await state.set_state(OrderClothes.show_clothes)
    current_state = await state.get_state()
    print(current_state)
    await message.answer(hbold("Ищу ваш товар в каталоге..."))

    product_name = get_args_from_message(message)
    link_in_shop = get_product_link_in_shop(product_name)
    filename, product_json_str = parser.run(link_in_shop, save_to_file=True)  # Получаем JSON в виде строки
    product_json = json.loads(product_json_str)  # Преобразуем строку в словарь
    await send_product_info(message, product_json)
    await state.set_state(OrderClothes.choose_size)

@router.callback_query(is_size_callback)
async def process_size_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if "selected_size" in user_data:
        await callback_query.message.answer("Вы уже выбрали размер товара.")
    else:
        selected_size = callback_query.data.replace('size_', '')
        await state.update_data(selected_size=selected_size)  # Сохранение выбранного размера
        await callback_query.message.answer(
            text=f"{selected_size}-й размер, отлично! Теперь выберите <b>способ оплаты</b>💲:",
            reply_markup=get_payment_keyboard()
        )
        await state.set_state(OrderClothes.choose_payment_method)  # Переход к выбору способа оплаты
    await callback_query.answer()

    user_data = await state.get_data() # Извлечение данных из контекста состояния
    selected_size = user_data.get('selected_size')
    print(f"Сохраненный размер одежды: {selected_size}")

@router.callback_query(is_payment_callback)
async def process_payment_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if "payment_method" in user_data:
        await callback_query.message.answer("Вы уже выбрали способ оплаты.")
    else:
        payment_method = callback_query.data.split('_')[-1]  # Извлекаем метод оплаты из callback_data
        await state.update_data(payment_method=payment_method)  # Сохраняем выбранный способ оплаты
        await callback_query.message.answer(f"Способ оплаты <b>{payment_method.capitalize()}</b> выбран.")
        await state.set_state(OrderClothes.choose_delivery_method)

    await callback_query.answer()
    await callback_query.message.answer("Выберите тип доставки:", reply_markup=get_delivery_keyboard())

def is_delivery_callback(callback_query: types.CallbackQuery) -> bool:
    """Проверяет, является ли callback_query выбором типа доставки."""
    return callback_query.data.startswith("delivery_")

@router.callback_query(is_delivery_callback)
async def process_delivery_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'delivery_method' in user_data:
        await callback_query.message.answer("Вы уже выбрали способ доставки: " + user_data["delivery_method"].replace('_', ' ').capitalize())
    else:
        delivery_method = callback_query.data.split("_")[1]  # Извлекаем тип доставки из callback_data
        await state.update_data(delivery_method=delivery_method)
        await state.set_state(PersonalDataForm.wait_for_name)
        await callback_query.message.answer("Выбран способ доставки: " + delivery_method.replace('_', ' ').capitalize())
    await state.set_state(PersonalDataForm.wait_for_name)
    await callback_query.message.answer("Введите ваше имя:")
    await callback_query.answer()
    
# Запрос имени
@router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer("Введите вашу фамилию:")

# Запрос фамилии
@router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.wait_for_email)
    await message.answer("Введите ваш email:")

# Запрос email
@router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer("Введите ваш номер телефона:")

# Запрос номера телефона
@router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(PersonalDataForm.wait_for_delivery_address)
    await message.answer("Введите адрес доставки:")

# Запрос адреса доставки
@router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    await state.update_data(delivery_address=message.text)
    user_data = await state.get_data()
    await state.clear()
    await message.answer(f"Спасибо, ваши данные:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\nEmail: {user_data['email']}\nТелефон: {user_data['phone_number']}\nАдрес доставки: {user_data['delivery_address']}\nВаши данные успешно сохранены, мы скоро свяжемся с вами!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())