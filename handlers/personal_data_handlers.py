from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import Validators
from states import PersonalDataForm
from keyboards import get_pay_keyboard
from json_text_for_bot import load_phrases_from_json_file

from aiogram import Router

personal_data_router = Router()

@personal_data_router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Обработка имени """
    INPUT_YOUR_NAME = load_phrases_from_json_file("INPUT_YOUR_NAME")
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_NAME)
        return 
    
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer("Введите вашу фамилию✒️:")

@personal_data_router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    INPUT_YOUR_SURNAME, INPUT_YOUR_EMAIL = load_phrases_from_json_file(
        "INPUT_YOUR_SURNAME",
        "INPUT_YOUR_EMAIL")
    """ Обработка фамилии. """
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_SURNAME)
        return 
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.wait_for_email)
    await message.answer(INPUT_YOUR_EMAIL)

@personal_data_router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    """ Обработка email. """
    INPUT_YOUR_EMAIL, INPUT_YOUR_EMAIL = load_phrases_from_json_file(
        "INPUT_YOUR_EMAIL",
        "INPUT_YOUR_EMAIL"
        )
    try:
        Validators.validate_email(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_EMAIL)
        return 
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer(INPUT_YOUR_EMAIL)

@personal_data_router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """ Обработка номера телефона. """
    INPUT_YOUR_PHONE, PHYSICAL_SHOP_ADDRESS, YOU_CAN_LIFT_YOUR_ORDER_FROM, INPUT_YOUR_ADDRESS = load_phrases_from_json_file(
        "INPUT_YOUR_PHONE",
        "PHYSICAL_SHOP_ADDRESS", 
        "YOU_CAN_LIFT_YOUR_ORDER_FROM",
        "INPUT_YOUR_ADDRESS")
    try:
        Validators.validate_phone_number(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_PHONE)
        return
    await state.update_data(phone_number=message.text)
    
    user_data = await state.get_data()
    if user_data.get("delivery_method") == 'delivery_pickup':
        # Если выбран самовывоз, выводим адрес и завершаем процесс
        await message.answer(YOU_CAN_LIFT_YOUR_ORDER_FROM + PHYSICAL_SHOP_ADDRESS)
        await state.clear()
    else:
        # Если требуется доставка, переходим к запросу адреса
        await state.set_state(PersonalDataForm.wait_for_delivery_address)
        await message.answer(INPUT_YOUR_ADDRESS)

@personal_data_router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    """ Обработка адреса. """
    PLEASE_INPUT_YOUR_FULL_ADDRESS = load_phrases_from_json_file("PLEASE_INPUT_YOUR_FULL_ADDRESS")
    try:
        Validators.validate_address(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + PLEASE_INPUT_YOUR_FULL_ADDRESS)
        return
    
    await state.update_data(delivery_address=message.text)
    user_data = await state.get_data()
    await message.answer(
        f"Спасибо, ваши <b>данные</b>:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\n"
        f"Email: {user_data['email']}\nТелефон: {user_data['phone_number']}\n"
        f"Адрес доставки: {user_data['delivery_address']}\nВаши данные успешно сохранены, мы скоро свяжемся с вами!"
    , reply_markup=get_pay_keyboard())