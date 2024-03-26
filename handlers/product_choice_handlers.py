import json
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import is_size_callback, is_payment_choice_callback, is_delivery_callback, get_product_content, get_args_from_message
from keyboards import get_delivery_keyboard, get_payment_keyboard
from create_links import get_product_link_in_shop
from bs_parser import WebPageParser
from states import OrderClothes, PersonalDataForm

from json_text_for_bot import load_phrases_from_json_file
from aiogram import Router

product_choice_router = Router()

parser = WebPageParser(debug=True, folder='products_json', can_upload_from_file=True)

async def process_start_command_or_callback(data: str, message: Message = None, state: FSMContext = None):
    """Логика обработки для команды /start и callback от inline-клавиатуры."""
    NO_AVAILABLE_SIZES, PLEASE_WAIT = load_phrases_from_json_file("NO_AVAILABLE_SIZES", "PLEASE_WAIT")

    await message.answer(PLEASE_WAIT)

    await state.set_state(OrderClothes.show_clothes) # Устанавливаем состояние показа карточки товара
    
    link_in_shop = get_product_link_in_shop(product_name=data)
    filename, product_json_str = parser.run(link_in_shop, save_to_file=True)
    product_json = json.loads(product_json_str)

    # сохраняем данные о товаре в стейт # 
    await state.update_data(product_price=product_json['price']) # сохраняем ссылку на товар
    await state.update_data(link_in_shop=product_json['url']) # сохраняем ссылку на товар
    #####################################

    message_text, photoes, size_keyboard = get_product_content(product_json)
    if photoes:
        await message.answer_media_group(photoes)
    if not size_keyboard:
        message_text.append(NO_AVAILABLE_SIZES)
    await message.answer(message_text, parse_mode='HTML', reply_markup=size_keyboard)
    await state.set_state(OrderClothes.choose_size)

@product_choice_router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    """Обработчик команды /start."""
    product_name = get_args_from_message(message)
    await state.clear() 
    await state.update_data(last_product_slug=product_name)
    await process_start_command_or_callback(product_name, message=message, state=state)

@product_choice_router.callback_query(lambda c: c.data and c.data.startswith('get_product'))
async def process_start_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик callback-кнопки, имитирующий команду /start с аргументом."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await process_start_command_or_callback(product_name, message=callback_query.message, state=state)
    await callback_query.answer()
    await state.clear()

@product_choice_router.callback_query(is_size_callback)
async def process_size_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """ Выбор размера одежды. """
    user_data = await state.get_data()
    NO_AVAILABLE_SIZES, NOW_CHOOSE_PAYMENT_METHOD = load_phrases_from_json_file(
        "NO_AVAILABLE_SIZES",
        "NOW_CHOOSE_PAYMENT_METHOD")

    if "selected_size" in user_data:
        await callback_query.message.answer(NO_AVAILABLE_SIZES)
    else:
        selected_size = callback_query.data.replace('size_', '')
        await state.update_data(selected_size=selected_size)  # Сохранение выбранного размера
        await callback_query.message.answer(
            text=f"<b>{selected_size}-й</b> {NOW_CHOOSE_PAYMENT_METHOD}:",
            reply_markup=get_payment_keyboard()
        )
        await state.set_state(OrderClothes.choose_payment_method)  # Переход к выбору способа оплаты
    await callback_query.answer()

@product_choice_router.callback_query(is_payment_choice_callback)
async def process_payment_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """ Выбор метода оплаты. """
    PAYMENT_METHODS, YOU_HAVE_ALREADY_SELECTED_PAYMENT_METHOD, PAYMENT_METHOD_HAVE_SELECTED, NOW_CHOOSE_DELIVERY_METHOD = load_phrases_from_json_file(
        "PAYMENT_METHODS",
        "YOU_HAVE_ALREADY_SELECTED_PAYMENT_METHOD",
        "PAYMENT_METHOD_HAVE_SELECTED",
        "NOW_CHOOSE_DELIVERY_METHOD")

    user_data = await state.get_data()
    if "payment_method" in user_data:
        await callback_query.message.answer(YOU_HAVE_ALREADY_SELECTED_PAYMENT_METHOD)
    else:
        payment_method = callback_query.data.split(':')[1]  # Извлекаем метод оплаты из callback_data
        readable_payment_method = PAYMENT_METHODS.get(payment_method, 'Не знаю...')
        await state.update_data(payment_method=payment_method)  # Сохраняем выбранный способ оплаты
        await callback_query.message.answer(f"{PAYMENT_METHOD_HAVE_SELECTED} <b>\"{readable_payment_method}\"</b>")
        await state.set_state(OrderClothes.choose_delivery_method)

    await callback_query.answer()
    await callback_query.message.answer(NOW_CHOOSE_DELIVERY_METHOD, reply_markup=get_delivery_keyboard())

@product_choice_router.callback_query(is_delivery_callback)
async def process_delivery_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """ Выбор способа доставки. """
    SHIPPING_METHODS, YOU_HAVE_ALREADY_SELECTED_DELIVERY_METHOD, DELIVERY_METHOD_HAVE_SELECTED, INPUT_YOUR_NAME = load_phrases_from_json_file(
        "SHIPPING_METHODS",
        "YOU_HAVE_ALREADY_SELECTED_DELIVERY_METHOD",
        "DELIVERY_METHOD_HAVE_SELECTED",
        "INPUT_YOUR_NAME"
        )
    user_data = await state.get_data()
    if 'delivery_method' in user_data:
        await callback_query.message.answer(YOU_HAVE_ALREADY_SELECTED_DELIVERY_METHOD + user_data["delivery_method"].replace('_', ' ').capitalize())
    else:
        delivery_method = callback_query.data  # Извлекаем тип доставки из callback_data
        delivery_readable =  SHIPPING_METHODS[delivery_method] # читаемая версия способа доставки
        await state.update_data(delivery_method=delivery_method)
        await state.set_state(PersonalDataForm.wait_for_name)
        await callback_query.message.answer(f"{DELIVERY_METHOD_HAVE_SELECTED} {delivery_readable}")
    await state.set_state(PersonalDataForm.wait_for_name)
    await callback_query.message.answer(INPUT_YOUR_NAME)
    await callback_query.answer()