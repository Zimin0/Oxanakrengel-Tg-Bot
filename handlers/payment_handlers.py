from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext

from states import PaymentState
from payment import Payment
from config import PAYMENT_METHODS
from utils import is_payment_callback

payment_router = Router()

payment = Payment()

@payment_router.callback_query(is_payment_callback)
async def process_pay_callback(callback_query: types.CallbackQuery, state:FSMContext):
    """ Обработка нажатия на кнопку "Оплатить" """
    await state.set_state(PaymentState.wait_for_payment)
    user_data = await state.get_data()
    payment_method = user_data.get('payment_method')
    if payment_method:
        readable_payment_method = PAYMENT_METHODS.get(payment_method)
    else:
        raise KeyError("Способ оплаты не сохранен в состоянии пользователя.")
    payment_link = payment.get_payment_link()
    await callback_query.message.answer(f"Ваш выбраный способ оплаты: {readable_payment_method}")
    await callback_query.message.answer(f"Вот ваша ссылка для оплаты: {payment_link}")

