import json
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from utils import is_size_callback, is_payment_callback, get_product_content, get_args_from_message
from keyboards import get_delivery_keyboard, get_payment_keyboard
from create_links import get_product_link_in_shop
from bs_parser import WebPageParser
from states import OrderClothes, PersonalDataForm


router = Router()
parser = WebPageParser(debug=True, folder='products_json', can_upload_from_file=True)

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
    message_text, photoes, size_keyboard = get_product_content(product_json)
    if photoes:
        await message.answer_media_group(photoes) # Отправка медиа в виде альбома
    if not size_keyboard:
        message_text.append("Нет доступных размеров.")
    await message.answer(message_text, parse_mode='HTML', reply_markup=size_keyboard) # Отправка текстового сообщения с инлайн-клавиатурой

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
    await callback_query.message.answer("Выберите тип получения товара", reply_markup=get_delivery_keyboard())

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
    
@router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Получает имя """
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer("Введите вашу фамилию:")

@router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    """ Получает фамилию """
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.wait_for_email)
    await message.answer("Введите ваш email:")

@router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    """ Получает email """
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer("Введите ваш номер телефона:")

@router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """ Получает телефон """
    await state.update_data(phone_number=message.text)
    await state.set_state(PersonalDataForm.wait_for_delivery_address)
    await message.answer("Введите адрес доставки:")

@router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    """ Получает адрес доставки """
    await state.update_data(delivery_address=message.text)
    user_data = await state.get_data()
    await state.clear()
    await message.answer(f"Спасибо, ваши данные:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\nEmail: {user_data['email']}\nТелефон: {user_data['phone_number']}\nАдрес доставки: {user_data['delivery_address']}\nВаши данные успешно сохранены, мы скоро свяжемся с вами!")