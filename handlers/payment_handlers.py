from aiogram import Router
from aiogram import types
from aiogram.types import LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from states import PaymentState
from payment import Payment
from config import PAYMENT_METHODS, DEBUG
from utils import is_payment_callback

payment_router = Router() 
payment = Payment()

@payment_router.callback_query(is_payment_callback)
async def process_pay_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка нажатия на кнопку 'Оплатить'."""
    await state.set_state(PaymentState.wait_for_payment)
    user_data = await state.get_data()
    
    payment_method = user_data.get('payment_method')
    if payment_method:
        readable_payment_method = PAYMENT_METHODS.get(payment_method, 'Неизвестный метод')
        payment_link = payment.get_payment_link()
        
        if DEBUG:
            await callback_query.message.answer(
                "Тестовый режим оплаты.\n"
                f"Ваш выбранный способ оплаты: {hbold(readable_payment_method)}\n"
                f"Тестовая ссылка для оплаты: {payment_link}\n\n"
            )
            await callback_query.message.answer("Оплата успешна! Спасибо за вашу покупку 🎀")
        else:
            # Реальный режим оплаты
            prices = [LabeledPrice(label="Тестовый товар", amount=10000)] # 100.00 рублей
            await callback_query.bot.send_invoice(
                chat_id=callback_query.from_user.id,
                title="Тестовый товар",
                description="Описание тестового товара",
                provider_token=payment.get_provider_token(),
                currency="RUB",
                prices=prices,
                start_parameter="create_invoice_test",
                payload="Custom-Payload"
            )
    else:
        await callback_query.message.answer("Произошла ошибка при выборе способа оплаты.")

@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """Обработчик предварительного запроса на проверку от Telegram."""
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@payment_router.message()
async def successful_payment(message: types.Message):
    """Обработчик успешной оплаты."""
    if message.successful_payment:
        await message.answer("Спасибо за покупку!")
