from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import is_support_callback, is_support_message_confirmation_callback, Validators
from keyboards import get_last_product_keyboard, get_confirmation_support_keyboard
from states import SupportForm
from json_text_for_bot import load_phrases_from_json_file
from httpx_requests.support import create_support_request

support_router = Router()

from handlers.product_choice_handlers import process_start_command_or_callback

@support_router.callback_query(is_support_callback)
async def process_support_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Оставьте свое <b>сообщение в тех. поддержку</b>:')
    await state.set_state(SupportForm.wait_for_message)

@support_router.message(SupportForm.wait_for_message)
async def process_support_message(message: Message, state: FSMContext):
    """ Приглашение ввести текстовый запрос в тех.поддержку. """
    LEAVE_YOUR_MESSAGE_TO_TECH, SEND_REQUEST = load_phrases_from_json_file(
        "LEAVE_YOUR_MESSAGE_TO_TECH",
        "SEND_REQUEST")
    try:
        Validators.validate_support_message(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + LEAVE_YOUR_MESSAGE_TO_TECH)
        return 
    await state.update_data(support_message=message.text)
    await state.set_state(SupportForm.wait_for_confirmation)
    short_text = message.text[:40] + '...'
    keyboard = get_confirmation_support_keyboard()
    await message.answer(f'{SEND_REQUEST} "{short_text}" ?', parse_mode='HTML', reply_markup=keyboard)

@support_router.callback_query(is_support_message_confirmation_callback)
async def process_support_confirm_message(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик подтверждения сообщения техподдержки с кнопкой возврата к последнему товару."""
    YOUR_REQUEST_IS_SAVED, YOUR_CAN_RETURN_TO_THE_LAST_PRODUCT = load_phrases_from_json_file(
        "YOUR_REQUEST_IS_SAVED",
        "YOUR_CAN_RETURN_TO_THE_LAST_PRODUCT"
        )
    user_data = await state.get_data()
    ### Сохраняем в БД ### 
    user_telegram_tag = f"@{callback_query.from_user.username}"
    text = user_data['support_message']
    await create_support_request(
        user_id=user_telegram_tag,
        text=text
        )
    ######################
    await callback_query.message.answer(YOUR_REQUEST_IS_SAVED)
    user_data = await state.get_data()
    keyboard = get_last_product_keyboard(product_name=user_data.get('last_product_slug'))
    await callback_query.message.answer(YOUR_CAN_RETURN_TO_THE_LAST_PRODUCT, reply_markup=keyboard)
    await callback_query.answer()

@support_router.callback_query(lambda c: c.data and c.data.startswith("last_product"))
async def process_last_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик нажатия на inline кнопку последнего просмотренного товара."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await process_start_command_or_callback(product_name, callback_query=callback_query, state=state)
    await callback_query.answer()