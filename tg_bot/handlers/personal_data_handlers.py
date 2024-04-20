from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import Validators, parse_price_and_valute
from states import PersonalDataForm
from keyboards import get_pay_keyboard
from json_text_for_bot import load_phrases_from_json_file
from config import DEBUG, PAYMENT_TEST_MODE

from aiogram import Router
from httpx_requests.personal_data import get_or_create_personal_data
from httpx_requests.bot_order import create_bot_order
from httpx_requests.user_settings import get_user_setting

personal_data_router = Router()

@personal_data_router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Обработка имени """
    INPUT_YOUR_NAME, INPUT_YOUR_SURNAME = load_phrases_from_json_file(
        "INPUT_YOUR_NAME",
        "INPUT_YOUR_SURNAME"
        )
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_NAME)
        return 
    
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer(INPUT_YOUR_SURNAME)

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
    INPUT_YOUR_EMAIL, INPUT_YOUR_PHONE = load_phrases_from_json_file(
        "INPUT_YOUR_EMAIL",
        "INPUT_YOUR_PHONE"
        )
    try:
        Validators.validate_email(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + INPUT_YOUR_EMAIL)
        return 
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer(INPUT_YOUR_PHONE)

@personal_data_router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """ Обработка номера телефона. """
    INPUT_YOUR_PHONE, YOU_CAN_LIFT_YOUR_ORDER_FROM, INPUT_YOUR_ADDRESS = load_phrases_from_json_file(
        "INPUT_YOUR_PHONE",
        "YOU_CAN_LIFT_YOUR_ORDER_FROM",
        "INPUT_YOUR_ADDRESS")
    
    # Получаем адрес из модели настроек пользователя в БД
    PHYSICAL_SHOP_ADDRESS = await get_user_setting("PHYSICAL_SHOP_ADDRESS", "Москва, ул. Примерная, д. 10, 3 этаж")
    
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
        await message.answer(
        f"Спасибо, ваши <b>данные</b>:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\n"
        f"Email: {user_data['email']}\nТелефон: {user_data['phone_number']}\n"
        f"\nВаши данные успешно сохранены, мы скоро свяжемся с вами!"
    , reply_markup=get_pay_keyboard())
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
    price, valute = parse_price_and_valute(user_data.get('product_price')) # парсим цену товара

    delivery_type = user_data.get("delivery_method")

    if delivery_type == 'delivery_moscow': # Доставка по Москве
        slug = 'PRICE_DELIVERY_MOSCOW'
    elif delivery_type ==  'delivery_russia': # Доставка по России
        slug = 'PRICE_DELIVERY_RUSSIA'

    PRICE_FOR_DELIVERY = await get_user_setting(slug, 0.0)
    print('-------------------------------')
    print(f"{PRICE_FOR_DELIVERY}")
    print('-------------------------------')
    PRICE_FOR_DELIVERY = float(PRICE_FOR_DELIVERY['value'])

    total_price = float(price+PRICE_FOR_DELIVERY)
    print(f"Финальная цена заказа: {total_price}")

    ### Сохраняем в БД ### 
    price(f"Данные текущего пользователя: {user_data.get('name')}, {user_data.get('surname')}, {user_data.get('email')}")
    if not DEBUG:
        person_db_id = await get_or_create_personal_data(
            telegram_user_id=f"@{message.from_user.username}",
            name=user_data.get('name'), 
            surname=user_data.get('surname'), 
            address=user_data.get('delivery_address'), 
            email=user_data.get('email'), 
            phone_number=user_data.get('phone_number')
            )
        order_db_id = await create_bot_order(
            personal_data_id=person_db_id, 
            product_link=user_data.get('link_in_shop'), 
            size=user_data.get('selected_size'), 
            shipping_method=user_data.get('delivery_method'), 
            payment_method=user_data.get('payment_method'), 
            price=total_price, 
            status='waiting_for_payment',
            is_real_order=(not PAYMENT_TEST_MODE)
            )
        await state.update_data(product_price=f"{total_price} руб") # сохраняем стоимость товара + доставка
        await state.update_data(order_db_id=order_db_id) # сохраняем django_id заказа в состояние.
    ######################
    await message.answer(
        f"Спасибо, ваши <b>данные</b>:\n<b>🔹 Имя</b>: {user_data['name']}\n<b>🔹 Фамилия</b>: {user_data['surname']}\n"
        f"<b>🔹 Email</b>: {user_data['email']}\n<b>🔹 Телефон</b>: {user_data['phone_number']}\n"
        f"🟢 Цена с учетом доставки: <b>{total_price} руб.</b> \n"
        f"<b>🔹 Адрес доставки</b>: {user_data['delivery_address']}\nВаши данные <b>успешно сохранены</b>, мы скоро свяжемся с вами!"
    , reply_markup=get_pay_keyboard())