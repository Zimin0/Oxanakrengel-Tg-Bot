import json
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import is_size_callback, is_payment_choice_callback, is_delivery_callback, get_product_content, get_args_from_message, is_back_callback, show_state_data
from keyboards import get_delivery_keyboard, get_payment_keyboard, get_sizes_keyboard
from create_links import get_product_link_in_shop
from json_text_for_bot import load_phrases_from_json_file
from handlers.personal_data_handlers import display_name_choice,  display_delivery_address_choice, display_surname_choice, display_email_choice, display_phone_choice
from bs_parser import WebPageParser
from states import OrderClothes, PersonalDataForm

product_choice_router = Router()

parser = WebPageParser(debug=True, folder='products_json', can_upload_from_file=True)

#########################################################################################################
####################################### ПОКАЗ ТОВАРА ПОЛЬЗОВАТЕЛЮ #######################################
#########################################################################################################

@product_choice_router.callback_query(lambda c: c.data and c.data.startswith('get_product'))
async def process_start_callback(callback_query: CallbackQuery, state: FSMContext):
    """Обработчик callback-кнопки после отправки письма в тех.поддержку, имитирующий команду /start с аргументом."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await show_state_data(state, process_start_callback) # Вывод данных о состоянии
    await process_start_command_or_callback(product_name, message=callback_query.message, state=state)
    await callback_query.answer()
    await state.clear()

@product_choice_router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):
    """Обработчик команды /start c аргументом."""
    product_name = get_args_from_message(message)
    await state.clear() 
    await state.update_data(last_product_slug=product_name)
    await process_start_command_or_callback(message=message, state=state, product_name=product_name)

async def process_start_command_or_callback(message: Message = None, state: FSMContext = None, product_name: str = None):
    """Логика обработки для команды /start и callback от inline-клавиатуры."""
    PLEASE_WAIT = load_phrases_from_json_file("PLEASE_WAIT")
    await show_state_data(state, process_start_command_or_callback) # Вывод данных о состоянии
    await message.answer(PLEASE_WAIT) # вывод сообщени о ожидании
    await state.set_state(OrderClothes.show_clothes) # Устанавливаем состояние показа карточки товара
    
    link_in_shop = get_product_link_in_shop(product_name=product_name)
    filename, product_json_str = parser.run(link_in_shop, save_to_file=True)
    product_json = json.loads(product_json_str)

    # сохраняем данные о товаре в стейт # 
    await state.update_data(product_price=product_json['price']) # сохраняем цену на товар
    await state.update_data(link_in_shop=product_json['url']) # сохраняем ссылку на товар
    await state.update_data(product_title=product_json['title']) # сохраняем читаемое название товара
    await state.update_data(product_sizes=product_json['sizes'])
    #####################################

    NO_AVAILABLE_SIZES = load_phrases_from_json_file("NO_AVAILABLE_SIZES")
    message_text, photoes, size_keyboard = get_product_content(product_json)
    if photoes:
        await message.answer_media_group(photoes)
    if size_keyboard is None:
        message_text += f"{NO_AVAILABLE_SIZES}\n"
    await message.answer(message_text, parse_mode='HTML')

    await display_size_choice(message, state)

#########################################################################################################
############################################ РАЗМЕР ОДЕЖДЫ ##############################################
#########################################################################################################

async def display_size_choice(event, state: FSMContext):
    """ Выводит блок выбора размера одежды. """
    NO_AVAILABLE_SIZES, CHOOSE_SIZE = load_phrases_from_json_file("NO_AVAILABLE_SIZES", "CHOOSE_SIZE")
    await show_state_data(state, display_size_choice) # Вывод данных о состоянии
    user_data = await state.get_data()
    product_sizes = user_data.get('product_sizes')  # получаем доступные размеры одежды
    size_keyboard = get_sizes_keyboard(product_sizes)  # генерируем клавиатуру с размерами

    if size_keyboard is None:
        CHOOSE_SIZE = f"{NO_AVAILABLE_SIZES}\n"
    
    # Проверяем, является ли 'event' сообщением или обратным вызовом
    if isinstance(event, types.Message):
        await event.answer(CHOOSE_SIZE, parse_mode='HTML', reply_markup=size_keyboard)
    elif isinstance(event, types.CallbackQuery):
        await event.message.answer(CHOOSE_SIZE, parse_mode='HTML', reply_markup=size_keyboard) # TODO edit_text
        await event.answer()
    await state.set_state(OrderClothes.choose_size)

@product_choice_router.callback_query(is_size_callback)
async def process_size_callback(callback_query: CallbackQuery, state: FSMContext):
    """ Обработка нажатия кнопки выбора размера одежды. """
    YOU_HAVE_CHOSEN_SIZE = load_phrases_from_json_file("YOU_HAVE_CHOSEN_SIZE")
    await show_state_data(state, process_size_callback) # Вывод данных о состоянии

    selected_size = callback_query.data.replace('size_', '') # Извлекаем размер из callback_data
    await state.update_data(selected_size=selected_size) # Сохранение выбранного размера
    await callback_query.message.answer(f" {YOU_HAVE_CHOSEN_SIZE} <b>{selected_size}-й</b>") # Вывод сообщения для юзера, что размер выбран
    await display_payment_choice(callback_query, state)

#########################################################################################################
################################################ ОПЛАТА #################################################
#########################################################################################################

async def display_payment_choice(callback_query: CallbackQuery, state: FSMContext):
    """ Выводит блок выбора метода оплаты. """
    NOW_CHOOSE_PAYMENT_METHOD = load_phrases_from_json_file("NOW_CHOOSE_PAYMENT_METHOD")
    await show_state_data(state, display_payment_choice) # Вывод данных о состоянии
    await state.set_state(OrderClothes.choose_payment_method)  # Переход к выбору способа оплаты
    await callback_query.message.answer(text=f"{NOW_CHOOSE_PAYMENT_METHOD}:", reply_markup=get_payment_keyboard())
    await callback_query.answer()
    
@product_choice_router.callback_query(is_payment_choice_callback)
async def process_payment_callback(callback_query: CallbackQuery, state: FSMContext):
    """ Обработка нажатия на кнопку выбора метода оплаты. """
    PAYMENT_METHODS, PAYMENT_METHOD_HAVE_SELECTED = load_phrases_from_json_file(
        "PAYMENT_METHODS",
        "PAYMENT_METHOD_HAVE_SELECTED")
    
    await show_state_data(state, process_payment_callback) # Вывод данных о состоянии

    payment_method = callback_query.data.split(':')[1] # Извлекаем метод оплаты из callback_data
    readable_payment_method = PAYMENT_METHODS.get(payment_method, 'Не знаю...')
    ##### Блокировка метода PayPal #####
    if payment_method == "paypal":
        await callback_query.answer()
        return
    ####################################
    await state.update_data(payment_method=payment_method)  # Сохраняем выбранный способ оплаты
    await callback_query.message.answer(f"{PAYMENT_METHOD_HAVE_SELECTED} <b>\"{readable_payment_method}\"</b>")
    await display_delivery_choice(callback_query, state)

#########################################################################################################
############################################### ДОСТАВКА ################################################
#########################################################################################################

async def display_delivery_choice(callback_query: CallbackQuery, state: FSMContext):
    """ Выводит блок выбора метода доставки. """
    NOW_CHOOSE_DELIVERY_METHOD = load_phrases_from_json_file("NOW_CHOOSE_DELIVERY_METHOD")
    await show_state_data(state, display_delivery_choice) # Вывод данных о состоянии
    await state.set_state(OrderClothes.choose_delivery_method)
    await callback_query.message.answer(NOW_CHOOSE_DELIVERY_METHOD, reply_markup=get_delivery_keyboard())
    await callback_query.answer()

@product_choice_router.callback_query(is_delivery_callback)
async def process_delivery_callback(callback_query: CallbackQuery, state: FSMContext):
    """ Выбор способа доставки. """
    SHIPPING_METHODS, DELIVERY_METHOD_HAVE_SELECTED = load_phrases_from_json_file(
        "SHIPPING_METHODS",
        "DELIVERY_METHOD_HAVE_SELECTED",
        )
    await show_state_data(state, process_delivery_callback) # Вывод данных о состоянии

    delivery_method = callback_query.data  # Извлекаем тип доставки из callback_data
    delivery_readable = SHIPPING_METHODS[delivery_method] # читаемая версия способа доставки
    await state.update_data(delivery_method=delivery_method)
    await state.set_state(PersonalDataForm.wait_for_name)
    await callback_query.message.answer(f"{DELIVERY_METHOD_HAVE_SELECTED} {delivery_readable}")

    await display_name_choice(callback_query, state) 


# TODO перенести куда-то в другое место 

# Список состояний
state_order = [
    OrderClothes.show_clothes.state,
    OrderClothes.choose_size.state,
    OrderClothes.choose_payment_method.state,
    OrderClothes.choose_delivery_method.state,
    PersonalDataForm.wait_for_name.state,
    PersonalDataForm.wait_for_surname.state,
    PersonalDataForm.wait_for_email.state,
    PersonalDataForm.wait_for_phone_number.state,
    PersonalDataForm.wait_for_delivery_address.state
]

# Словарь обработчиков
state_handlers = {
    OrderClothes.choose_size: display_size_choice,
    OrderClothes.choose_payment_method: display_payment_choice,
    OrderClothes.choose_delivery_method: display_delivery_choice,
    PersonalDataForm.wait_for_name: display_name_choice,
    PersonalDataForm.wait_for_surname: display_surname_choice,
    PersonalDataForm.wait_for_email: display_email_choice,
    PersonalDataForm.wait_for_phone_number: display_phone_choice,
    PersonalDataForm.wait_for_delivery_address: display_delivery_address_choice
}

@product_choice_router.callback_query(is_back_callback)
async def back_button_handler(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    state_index = state_order.index(current_state) if current_state else -1
    print(f"Текущее состояние: {current_state}")
    if state_index > 0:
        # Определяем предыдущее состояние
        previous_state = state_order[state_index - 1]
        await state.set_state(previous_state)
        print(f"Переключаю в состояние: {previous_state}")
        # Вызываем обработчик для предыдущего состояния
        handler = state_handlers[previous_state]
        await handler(callback_query, state)
    else:
        # Сообщение пользователю
        await callback_query.message.answer("Вы находитесь в начальном этапе и не можете вернуться назад.")

    await callback_query.answer()
