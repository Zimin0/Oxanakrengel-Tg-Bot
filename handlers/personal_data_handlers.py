from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import Validators, parse_price_and_valute, show_state_data
from states import PersonalDataForm
from keyboards import get_pay_keyboard, create_back_button_keyboard
from json_text_for_bot import load_phrases_from_json_file
from config import PAYMENT_TEST_MODE, DISABLE_VALIDATION, debug_data_for_personal, debug_data_for_order

from aiogram import Router
from httpx_requests.personal_data import get_or_create_personal_data
from httpx_requests.bot_order import create_bot_order
from httpx_requests.user_settings import get_user_setting

personal_data_router = Router()

#########################################################################################################
################################################# ИМЯ ########################№№№########################
#########################################################################################################

async def display_name_choice(event, state: FSMContext):
    """ Выводит блок ввода имени. """
    INPUT_YOUR_NAME = load_phrases_from_json_file("INPUT_YOUR_NAME")
    await state.set_state(PersonalDataForm.wait_for_name)
    await show_state_data(state, display_name_choice) # Вывод данных о состоянии
    
    # Проверяем, является ли 'event' сообщением или callback
    if isinstance(event, Message):
        await event.answer(INPUT_YOUR_NAME, reply_markup=create_back_button_keyboard())
    elif isinstance(event, CallbackQuery):
        # Используем 'message.answer' для ответа на оригинальное сообщение.
        await event.message.answer(INPUT_YOUR_NAME, reply_markup=create_back_button_keyboard())
        await event.answer()

@personal_data_router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Обработка имени """
    await show_state_data(state, process_name) # Вывод данных о состоянии
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n")
        await display_name_choice(message, state)
        return 
    await state.update_data(name=message.text)
    await display_surname_choice(message, state)

#########################################################################################################
############################################### ФАМИЛИЯ #################################################
#########################################################################################################

async def display_surname_choice(event, state: FSMContext):
    """ Выводит блок ввода фамилии. """
    INPUT_YOUR_SURNAME = load_phrases_from_json_file("INPUT_YOUR_SURNAME")
    await state.set_state(PersonalDataForm.wait_for_surname)
    await show_state_data(state, display_surname_choice)  # Вывод данных о состоянии
    reply_markup = create_back_button_keyboard()

    if isinstance(event, Message):
        await event.answer(INPUT_YOUR_SURNAME, reply_markup=reply_markup)
    elif isinstance(event, CallbackQuery):
        await event.message.answer(INPUT_YOUR_SURNAME, reply_markup=reply_markup)
        await event.answer()


@personal_data_router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    """ Обработка фамилии. """ 
    await show_state_data(state, process_surname) # Вывод данных о состоянии
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n")
        await display_surname_choice(message, state)
        return 
    await state.update_data(surname=message.text)

    await display_email_choice(message, state)

#########################################################################################################
################################################ ПОЧТА ##################################################
#########################################################################################################

async def display_email_choice(event, state: FSMContext):
    """ Выводит блок ввода почты. """
    INPUT_YOUR_EMAIL = load_phrases_from_json_file("INPUT_YOUR_EMAIL")
    await state.set_state(PersonalDataForm.wait_for_email)
    await show_state_data(state, display_email_choice)  # Вывод данных о состоянии
    reply_markup = create_back_button_keyboard()

    if isinstance(event, Message):
        await event.answer(INPUT_YOUR_EMAIL, reply_markup=reply_markup)
    elif isinstance(event, CallbackQuery):
        await event.message.answer(INPUT_YOUR_EMAIL, reply_markup=reply_markup)
        await event.answer()


@personal_data_router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    """ Обработка ввода почты. """
    await show_state_data(state, process_email) # Вывод данных о состоянии
    try:
        Validators.validate_email(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n")
        await display_email_choice(message, state)
        return 
    await state.update_data(email=message.text)

    await display_phone_choice(message, state)

#########################################################################################################
############################################### ТЕЛЕФОН #################################################
#########################################################################################################

async def display_phone_choice(event, state: FSMContext):
    """ Выводит блок ввода телефона. """
    INPUT_YOUR_PHONE = load_phrases_from_json_file("INPUT_YOUR_PHONE")
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await show_state_data(state, display_phone_choice)  # Вывод данных о состоянии
    reply_markup = create_back_button_keyboard()

    if isinstance(event, Message):
        await event.answer(INPUT_YOUR_PHONE, reply_markup=reply_markup)
    elif isinstance(event, CallbackQuery):
        await event.message.answer(INPUT_YOUR_PHONE, reply_markup=reply_markup)
        await event.answer()

@personal_data_router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    """ Обработка ввода номера телефона. """
    await show_state_data(state, process_phone_number) # Вывод данных о состоянии
    try:
        Validators.validate_phone_number(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n")
        await display_phone_choice(message, state)
        return
    await state.update_data(phone_number=message.text)

    #### Смотрим, нужно ли запрашивать адрес у клиента ####
    user_data = await state.get_data()
    if user_data.get("delivery_method") == 'DELIVERY_PICKUP': # самовывоз - адрес клиента не требуется
        await display_result_data(message, state) # выводим собранную информацию
    else: # требуется адрес клиента для доставки
        await display_delivery_address_choice(message, state)

#########################################################################################################
################################################ АДРЕС ##################################################
#########################################################################################################

async def display_delivery_address_choice(event, state: FSMContext):
    """ Выводит блок ввода адреса. """
    INPUT_YOUR_ADDRESS = load_phrases_from_json_file("INPUT_YOUR_ADDRESS")
    await state.set_state(PersonalDataForm.wait_for_delivery_address)
    await show_state_data(state, display_delivery_address_choice)  # Вывод данных о состоянии
    reply_markup = create_back_button_keyboard()

    if isinstance(event, Message):
        await event.answer(INPUT_YOUR_ADDRESS, reply_markup=reply_markup)
    elif isinstance(event, CallbackQuery):
        await event.message.answer(INPUT_YOUR_ADDRESS, reply_markup=reply_markup)
        await event.answer()

@personal_data_router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    """ Обработка ввода адреса. """  
    await show_state_data(state, process_delivery_address) # Вывод данных о состоянии
    try:
        Validators.validate_address(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n")
        await display_delivery_address_choice(message, state)
    await state.update_data(delivery_address=message.text) 
    await display_result_data(message, state) # выводим собранную информацию

#########################################################################################################
################################################ ОПЛАТА #################################################
#########################################################################################################

async def display_result_data(message: Message, state: FSMContext):
    """ Выводит собранную у пользователя информацию. """
    await show_state_data(state, display_result_data) # Вывод данных о состоянии
    YOU_CAN_LIFT_YOUR_ORDER_FROM, \
    THANKS_FOR_YOUR_DATA, \
    YOUR_NAME, \
    YOUR_SURNAME, \
    YOUR_EMAIL, \
    YOUR_PHONE, \
    YOUR_PRICE, \
    YOUR_ADDRESS, \
    YOUR_DATA_WAS_SAVED = load_phrases_from_json_file(
        "YOU_CAN_LIFT_YOUR_ORDER_FROM",
        "THANKS_FOR_YOUR_DATA",
        "YOUR_NAME",
        "YOUR_SURNAME",
        "YOUR_EMAIL",
        "YOUR_PHONE",
        "YOUR_PRICE",
        "YOUR_ADDRESS",
        "YOUR_DATA_WAS_SAVED",
        )
    user_data = await state.get_data()
    price, valute = parse_price_and_valute(user_data.get('product_price')) # парсим цену товара

    if user_data.get("delivery_method") == 'DELIVERY_PICKUP': # Если самовывоз #
        ### Получаем адрес из модели настроек пользователя в БД ###
        PHYSICAL_SHOP_ADDRESS = await get_user_setting("PHYSICAL_SHOP_ADDRESS", "Адрес неизвестен, обратитесь в поддержку.")
        PHYSICAL_SHOP_ADDRESS = PHYSICAL_SHOP_ADDRESS['value']
        total_price = float(price)
        delivery_or_pickup_string = f"{YOU_CAN_LIFT_YOUR_ORDER_FROM}\n\n<b>{PHYSICAL_SHOP_ADDRESS}</b>\n"

    else: # Если доставка на адрес #
        ########## Добавляем к сумме стоимость доставки ###########
        delivery_type = user_data.get("delivery_method")
        __slug_for_delivery_price = f"PRICE_{delivery_type}" # В БД они хранятся как PRICE_DELIVERY_MOSCOW

        PRICE_FOR_DELIVERY = await get_user_setting(__slug_for_delivery_price, 0.0)
        PRICE_FOR_DELIVERY = float(PRICE_FOR_DELIVERY['value'])

        total_price = float(price + PRICE_FOR_DELIVERY)
        delivery_or_pickup_string = f"{YOUR_ADDRESS} {user_data['delivery_address']}"

    await state.update_data(total_price=total_price) # сохраняем окончательную сумму заказа
    await __save_data_to_db(message, state) # сохраняем данные о заказе в БД #
    await message.answer(
        f"{THANKS_FOR_YOUR_DATA}\n{YOUR_NAME} {user_data['name']}\n{YOUR_SURNAME} {user_data['surname']}\n"
        f"{YOUR_EMAIL} {user_data['email']}\n{YOUR_PHONE} {user_data['phone_number']}\n"
        f"{YOUR_PRICE} <b>{total_price} руб.</b> \n"
        f"{delivery_or_pickup_string}\n\n"
        f"{YOUR_DATA_WAS_SAVED}"
    , reply_markup=get_pay_keyboard())

async def __save_data_to_db(message:Message, state: FSMContext):
    """ Сохраняtn в БД объект пользователя и создает новый заказ. """
    user_data = await state.get_data()
    total_price = user_data.get('total_price')
    print(f"Финальная цена заказа: {total_price}")

    if DISABLE_VALIDATION: # Валидация выключена, поэтому сохраняем подготовленные тестовые данные
        person_db_id = await get_or_create_personal_data(**debug_data_for_personal)
        order_db_id = await create_bot_order(
            personal_data_id=person_db_id, 
            **debug_data_for_order
        )
    else: # Иначе боевой режим
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

    await state.update_data(product_price=f"{total_price} руб") # сохраняем стоимость товара + стоимость доставки
    await state.update_data(order_db_id=order_db_id) # сохраняем django_id заказа в состояние.










# @personal_data_router.message(PersonalDataForm.wait_for_phone_number)
# async def process_phone_number(message: Message, state: FSMContext):
#     """ Обработка номера телефона. """
#     INPUT_YOUR_PHONE, \
#     YOU_CAN_LIFT_YOUR_ORDER_FROM, \
#     INPUT_YOUR_ADDRESS, \
#     PLEASE_INPUT_YOUR_FULL_ADDRESS, \
#     THANKS_FOR_YOUR_DATA, \
#     YOUR_NAME, \
#     YOUR_SURNAME, \
#     YOUR_EMAIL, \
#     YOUR_PHONE, \
#     YOUR_PRICE, \
#     YOUR_ADDRESS, \
#     YOUR_DATA_WAS_SAVED = load_phrases_from_json_file(
#         "INPUT_YOUR_PHONE",
#         "YOU_CAN_LIFT_YOUR_ORDER_FROM",
#         "INPUT_YOUR_ADDRESS",
#         "PLEASE_INPUT_YOUR_FULL_ADDRESS",
#         "THANKS_FOR_YOUR_DATA",
#         "YOUR_NAME",
#         "YOUR_SURNAME",
#         "YOUR_EMAIL",
#         "YOUR_PHONE",
#         "YOUR_PRICE",
#         "YOUR_ADDRESS",
#         "YOUR_DATA_WAS_SAVED",
#         )
        
    
#     # Получаем адрес из модели настроек пользователя в БД
    # PHYSICAL_SHOP_ADDRESS = await get_user_setting("PHYSICAL_SHOP_ADDRESS", "Москва, ул. Примерная, д. 10, 3 этаж")
    # PHYSICAL_SHOP_ADDRESS = PHYSICAL_SHOP_ADDRESS['value']
    # try:
    #     Validators.validate_phone_number(message.text)
    # except ValueError as e:
    #     await message.answer(str(e) + "\n" + INPUT_YOUR_PHONE)
    #     return
    # await state.update_data(phone_number=message.text)
    
    # user_data = await state.get_data()

    # price, valute = parse_price_and_valute(user_data.get('product_price')) # парсим цену товара

    # if user_data.get("delivery_method") == 'DELIVERY_PICKUP':
    #     # Если выбран самовывоз, выводим адрес и завершаем процесс
    #     await message.answer(
    #         f"{THANKS_FOR_YOUR_DATA}\n{YOUR_NAME} {user_data['name']}\n{YOUR_SURNAME} {user_data['surname']}\n"
    #         f"{YOUR_EMAIL} {user_data['email']}\n{YOUR_PHONE} {user_data['phone_number']}\n"
    #         f"{YOUR_PRICE} <b>{float(price)} руб.</b> \n"
    #         f"{YOU_CAN_LIFT_YOUR_ORDER_FROM}\n\n<b>{PHYSICAL_SHOP_ADDRESS}</b>\n\n{YOUR_DATA_WAS_SAVED}"
    #     , reply_markup=get_pay_keyboard())  
    # else:
    #     # Если требуется доставка, переходим к запросу адреса
    #     await state.set_state(PersonalDataForm.wait_for_delivery_address)
    #     await message.answer(INPUT_YOUR_ADDRESS)

    ################################################################


# @personal_data_router.message(PersonalDataForm.wait_for_delivery_address)
# async def process_delivery_address(message: Message, state: FSMContext):
#     """ Обработка адреса. """
#     PLEASE_INPUT_YOUR_FULL_ADDRESS, THANKS_FOR_YOUR_DATA, YOUR_NAME, YOUR_SURNAME, YOUR_EMAIL, YOUR_PHONE, YOUR_PRICE, YOUR_ADDRESS, YOUR_DATA_WAS_SAVED = load_phrases_from_json_file(
#         "PLEASE_INPUT_YOUR_FULL_ADDRESS",
#         "THANKS_FOR_YOUR_DATA",
#         "YOUR_NAME",
#         "YOUR_SURNAME",
#         "YOUR_EMAIL",
#         "YOUR_PHONE",
#         "YOUR_PRICE",
#         "YOUR_ADDRESS",
#         "YOUR_DATA_WAS_SAVED",
#         )
    
    # try:
    #     Validators.validate_address(message.text)
    # except ValueError as e:
    #     await message.answer(str(e) + "\n" + PLEASE_INPUT_YOUR_FULL_ADDRESS)
    #     return

    ### Обновляем адрес доставки ###
    # await state.update_data(delivery_address=message.text) 

    # user_data = await state.get_data()
    
    ### парсим цену товара ###
    # price, valute = parse_price_and_valute(user_data.get('product_price'))
    # delivery_type = user_data.get("delivery_method")
    # slug_for_delivery_price = f"PRICE_{delivery_type}" # В БД они хранятся как PRICE_DELIVERY_MOSCOW

    # PRICE_FOR_DELIVERY = await get_user_setting(slug_for_delivery_price, 0.0)
    # PRICE_FOR_DELIVERY = float(PRICE_FOR_DELIVERY['value'])

    # total_price = float(price + PRICE_FOR_DELIVERY)
    # print(f"Финальная цена заказа: {total_price}")


    # user_data = await state.get_data()
    # total_price = user_data.get('total_price')

    # ### Сохраняем в БД объект пользователя и создаем новый заказ ### 
    # if DISABLE_VALIDATION: # Валидация выключена, поэтому сохраняем подготовленные тестовые данные
    #     person_db_id = await get_or_create_personal_data(**debug_data_for_personal)
    #     order_db_id = await create_bot_order(
    #         personal_data_id=person_db_id, 
    #         **debug_data_for_order
    #     )
    # else: # Иначе боевой режим
    #     person_db_id = await get_or_create_personal_data(
    #         telegram_user_id=f"@{message.from_user.username}",
    #         name=user_data.get('name'), 
    #         surname=user_data.get('surname'), 
    #         address=user_data.get('delivery_address'), 
    #         email=user_data.get('email'), 
    #         phone_number=user_data.get('phone_number')
    #     )
    #     order_db_id = await create_bot_order(
    #         personal_data_id=person_db_id, 
    #         product_link=user_data.get('link_in_shop'), 
    #         size=user_data.get('selected_size'),
    #         shipping_method=user_data.get('delivery_method'), 
    #         payment_method=user_data.get('payment_method'), 
    #         price=total_price, 
    #         status='waiting_for_payment',
    #         is_real_order=(not PAYMENT_TEST_MODE)
    #     )

    # await state.update_data(product_price=f"{total_price} руб") # сохраняем стоимость товара + стоимость доставки
    # await state.update_data(order_db_id=order_db_id) # сохраняем django_id заказа в состояние.
    ################################################################

    # await message.answer(
    #     f"{THANKS_FOR_YOUR_DATA}\n{YOUR_NAME} {user_data['name']}\n{YOUR_SURNAME} {user_data['surname']}\n"
    #     f"{YOUR_EMAIL} {user_data['email']}\n{YOUR_PHONE} {user_data['phone_number']}\n"
    #     f"{YOUR_PRICE} <b>{total_price} руб.</b> \n"
    #     f"{YOUR_ADDRESS} {user_data['delivery_address']}\n{YOUR_DATA_WAS_SAVED}"
    # , reply_markup=get_pay_keyboard())