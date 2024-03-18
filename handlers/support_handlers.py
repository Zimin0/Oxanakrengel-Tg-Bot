from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import is_support_callback, is_support_message_confirmation_callback, Validators
from keyboards import get_last_product_keyboard, get_confirmation_support_keyboard
from states import SupportForm

support_router = Router()

from handlers.product_choice_handlers import process_start_command_or_callback

@support_router.callback_query(is_support_callback)
async def process_support_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Оставьте свое <b>сообщение в тех. поддержку</b>:')
    await state.set_state(SupportForm.wait_for_message)

@support_router.message(SupportForm.wait_for_message)
async def process_support_message(message: Message, state: FSMContext):
    """ Приглашение ввести текстовый запрос в тех.поддержку. """
    try:
        Validators.validate_support_message(message.text)
    except ValueError as e:
        await message.answer(str(e) + "\n" + "Оставьте свое <b>сообщение в тех. поддержку</b> ✒️:")
        return 
    await state.update_data(support_message=message.text)
    await state.set_state(SupportForm.wait_for_confirmation)
    short_text = message.text[:40] + '...'
    keyboard = get_confirmation_support_keyboard()
    await message.answer(f'Отправить запрос: "{short_text}" ?', parse_mode='HTML', reply_markup=keyboard)

@support_router.callback_query(is_support_message_confirmation_callback)
async def process_support_confirm_message(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик подтверждения сообщения техподдержки с кнопкой возврата к последнему товару."""
    await callback_query.message.answer("Ваша заявка сохранена! Мы решим ее в ближайшее время ✅")
    user_data = await state.get_data()
    keyboard = get_last_product_keyboard(product_name=user_data.get('last_product_slug'))
    await callback_query.message.answer("Вы можете вернуться к <b>последнему товару</b>, нажав кнопку товара ниже ⬇️", reply_markup=keyboard)
    await callback_query.answer()

@support_router.callback_query(lambda c: c.data and c.data.startswith("last_product"))
async def process_last_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик нажатия на inline кнопку последнего просмотренного товара."""
    user_data = await state.get_data()
    product_name = user_data.get('last_product_slug')
    await process_start_command_or_callback(product_name, callback_query=callback_query, state=state)
    await callback_query.answer()