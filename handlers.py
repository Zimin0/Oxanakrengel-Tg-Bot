import json
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from utils import is_size_callback, is_payment_callback, is_support_callback, is_delivery_callback, get_product_content, get_args_from_message, is_support_message_confirmation_callback, Validators
from keyboards import get_delivery_keyboard, get_last_product_keyboard, get_confirmation_support_keyboard, get_payment_keyboard
from create_links import get_product_link_in_shop
from bs_parser import WebPageParser
from states import OrderClothes, PersonalDataForm, SupportForm
from config import PHYSICAL_SHOP_ADDRESS


router = Router()
parser = WebPageParser(debug=True, folder='products_json', can_upload_from_file=True)

##################### Обработчики #####################
async def process_start_command_or_callback(data: str, message: Message = None, state: FSMContext = None):
    """Логика обработки для команды /start и callback от inline-клавиатуры."""
    await state.set_state(OrderClothes.show_clothes)
    link_in_shop = get_product_link_in_shop(product_name=data)
    filename, product_json_str = parser.run(link_in_shop, save_to_file=True)
    product_json = json.loads(product_json_str)

    message_text, photoes, size_keyboard = get_product_content(product_json)
    if photoes:
        await message.answer_media_group(photoes)
    if not size_keyboard:
        message_text.append("Нет доступных размеров.")
    await message.answer(message_text, parse_mode='HTML', reply_markup=size_keyboard)
    await state.set_state(OrderClothes.choose_size)

@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    """Обработчик команды /start."""
    product_name = get_args_from_message(message)
    await state.clear() 
    await state.update_data(last_product_slug=product_name)
    await process_start_command_or_callback(product_name, message=message, state=state)

@router.callback_query(lambda c: c.data and c.data.startswith('get_product'))
async def process_start_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик callback-кнопки, имитирующий команду /start с аргументом."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await process_start_command_or_callback(product_name, message=callback_query.message, state=state)
    await callback_query.answer()

@router.callback_query(is_size_callback)
async def process_size_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if "selected_size" in user_data:
        await callback_query.message.answer("Вы уже выбрали <b>размер</b> товара.")
    else:
        selected_size = callback_query.data.replace('size_', '')
        await state.update_data(selected_size=selected_size)  # Сохранение выбранного размера
        await callback_query.message.answer(
            text=f"<b>{selected_size}-й</b> размер, отлично! Теперь выберите <b>способ оплаты</b>💲:",
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
        await callback_query.message.answer("Вы уже выбрали <b>способ оплаты</b>.")
    else:
        payment_method = callback_query.data.split('_')[-1]  # Извлекаем метод оплаты из callback_data
        await state.update_data(payment_method=payment_method)  # Сохраняем выбранный способ оплаты
        await callback_query.message.answer(f"Способ оплаты <b>{payment_method.capitalize()}</b> выбран.")
        await state.set_state(OrderClothes.choose_delivery_method)

    await callback_query.answer()
    await callback_query.message.answer("Выберите <b>способ получения товара</b>", reply_markup=get_delivery_keyboard())

@router.callback_query(is_delivery_callback)
async def process_delivery_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'delivery_method' in user_data:
        await callback_query.message.answer("Вы уже выбрали <b>способ доставки</b>: " + user_data["delivery_method"].replace('_', ' ').capitalize())
    else:
        delivery_method = callback_query.data  # Извлекаем тип доставки из callback_data
        await state.update_data(delivery_method=delivery_method)
        await state.set_state(PersonalDataForm.wait_for_name)
        await callback_query.message.answer("Выбран способ доставки: " + delivery_method.replace('_', ' ').capitalize())
    await state.set_state(PersonalDataForm.wait_for_name)
    await callback_query.message.answer("Введите ваше <b>имя</b>:")
    await callback_query.answer()
    
@router.message(PersonalDataForm.wait_for_name)
async def process_name(message: Message, state: FSMContext):
    """ Получает имя """
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваше <b>имя</b>:")
        return 
    
    await state.update_data(name=message.text)
    await state.set_state(PersonalDataForm.wait_for_surname)
    await message.answer("Введите вашу фамилию:")

@router.message(PersonalDataForm.wait_for_surname)
async def process_surname(message: Message, state: FSMContext):
    """ Получает фамилию """
    try:
        Validators.validate_name(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите вашу <b>фамилию</b>:")
        return 
    await state.update_data(surname=message.text)
    await state.set_state(PersonalDataForm.wait_for_email)
    await message.answer("Введите ваш <b>email</b>:")

@router.message(PersonalDataForm.wait_for_email)
async def process_email(message: Message, state: FSMContext):
    """ Получает email """
    try:
        Validators.validate_email(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваш <b>email</b>:")
        return 
    await state.update_data(email=message.text)
    await state.set_state(PersonalDataForm.wait_for_phone_number)
    await message.answer("Введите ваш <b>номер телефона</b>:")

@router.message(PersonalDataForm.wait_for_phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    try:
        Validators.validate_phone_number(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Введите ваш <b>телефон</b>:")
        return
    await state.update_data(phone_number=message.text)
    
    # Тут должна быть проверка на способ доставки
    user_data = await state.get_data()
    print(user_data.get("delivery_method") )
    if user_data.get("delivery_method") == 'delivery_pickup':
        # Если выбран самовывоз, выводим адрес и завершаем процесс
        await message.answer('Вы можете забрать свой заказ по <b>адресу</b>:\n' + PHYSICAL_SHOP_ADDRESS)
        await state.clear()  # Очистка состояния после завершения процесса
    else:
        # Если требуется доставка, переходим к запросу адреса
        await state.set_state(PersonalDataForm.wait_for_delivery_address)
        await message.answer("Введите <b>адрес</b> доставки:")

@router.message(PersonalDataForm.wait_for_delivery_address)
async def process_delivery_address(message: Message, state: FSMContext):
    try:
        Validators.validate_address(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\nПожалуйста, введите полный <b>адрес</b> доставки:")
        return
    
    # Если валидация прошла успешно, сохраняем адрес и выводим подтверждение
    await state.update_data(delivery_address=message.text)
    user_data = await state.get_data()
    
    # await state.clear()  # Очистка состояния после завершения процесса
    await message.answer(
        f"Спасибо, ваши <b>данные</b>:\nИмя: {user_data['name']}\nФамилия: {user_data['surname']}\n"
        f"Email: {user_data['email']}\nТелефон: {user_data['phone_number']}\n"
        f"Адрес доставки: {user_data['delivery_address']}\nВаши данные успешно сохранены, мы скоро свяжемся с вами!"
    )

@router.callback_query(is_support_callback)
async def process_support_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Оставьте свое сообщение в тех. поддержку далее: ')
    await state.set_state(SupportForm.wait_for_message)

@router.message(SupportForm.wait_for_message)
async def process_support_message(message: Message, state: FSMContext):
    await state.update_data(support_message=message.text)
    await state.set_state(SupportForm.wait_for_confirmation)
    short_text = message.text[:40] + '...'
    keyboard = get_confirmation_support_keyboard()
    await message.answer(f'Отправить запрос: "{short_text}" ?', parse_mode='HTML', reply_markup=keyboard)

@router.callback_query(is_support_message_confirmation_callback)
async def process_support_confirm_message(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик подтверждения сообщения техподдержки с кнопкой возврата к последнему товару."""
    await callback_query.message.answer("Ваша заявка сохранена! Мы решим ее в ближайшее время.")
    user_data = await state.get_data()
    keyboard = get_last_product_keyboard(product_name=user_data.get('last_product_slug'))
    await callback_query.message.answer("Вы можете вернуться к последнему товару, нажав кнопку товара ниже...", reply_markup=keyboard)
    await callback_query.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("last_product"))
async def process_last_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик нажатия на inline кнопку последнего просмотренного товара."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await process_start_command_or_callback(product_name, callback_query=callback_query, state=state)
    await callback_query.answer()