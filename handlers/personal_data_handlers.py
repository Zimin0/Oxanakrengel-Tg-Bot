from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import Validators
from states import PersonalDataForm
from config import PHYSICAL_SHOP_ADDRESS

from aiogram import Router

personal_data_router = Router()

@personal_data_router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Обработка имени """
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваше <b>имя</b> ✒️:")
        return 
    
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer("Введите вашу фамилию✒️:")

@personal_data_router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    """ Обработка фамилии. """
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите вашу <b>фамилию</b> ✒️:")
        return 
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.wait_for_email)
    await message.answer("Введите ваш <b>email</b>:")

@personal_data_router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    """ Обработка email. """
    try:
        Validators.validate_email(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваш <b>email</b> 📧:")
        return 
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer("Введите ваш <b>номер телефона</b>:")

@personal_data_router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """ Обработка номера телефона. """
    try:
        Validators.validate_phone_number(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваш <b>телефон</b> 📞:")
        return
    await state.update_data(phone_number=message.text)
    
    user_data = await state.get_data()
    if user_data.get("delivery_method") == 'delivery_pickup':
        # Если выбран самовывоз, выводим адрес и завершаем процесс
        await message.answer('Вы можете забрать свой заказ по <b>адресу</b> 🧱:\n' + PHYSICAL_SHOP_ADDRESS)
        await state.clear()
    else:
        # Если требуется доставка, переходим к запросу адреса
        await state.set_state(PersonalDataForm.wait_for_delivery_address)
        await message.answer("Введите <b>адрес</b> доставки 🧱:")

@personal_data_router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    """ Обработка адреса. """
    try:
        Validators.validate_address(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\nПожалуйста, введите полный <b>адрес</b> доставки 🧱:")
        return
    
    await state.update_data(delivery_address=message.text)
    user_data = await state.get_data()
    await message.answer(
        f"Спасибо, ваши <b>данные</b>:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\n"
        f"Email: {user_data['email']}\nТелефон: {user_data['phone_number']}\n"
        f"Адрес доставки: {user_data['delivery_address']}\nВаши данные успешно сохранены, мы скоро свяжемся с вами!"
    )