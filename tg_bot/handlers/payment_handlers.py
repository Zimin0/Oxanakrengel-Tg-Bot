from aiogram import Router
from aiogram import types
from aiogram.types import LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from states import PaymentState
from payment import Custom_Payment
from config import PAYMENT_TEST_MODE
from json_text_for_bot import load_phrases_from_json_file
from utils import is_payment_callback, parse_price_and_valute

payment_router = Router() 
payment = Custom_Payment()

@payment_router.callback_query(is_payment_callback)
async def process_pay_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка нажатия на кнопку 'Оплатить'."""
    PAYMENT_METHODS, PAYMENT_IS_SUCCESSFUL, ERROR_IN_PAYMENT = load_phrases_from_json_file(
        "PAYMENT_METHODS",
        "PAYMENT_IS_SUCCESSFUL",
        "ERROR_IN_PAYMENT"
    )
    await state.set_state(PaymentState.wait_for_payment)
    user_data = await state.get_data()
    
    payment_method = user_data.get('payment_method')
    if payment_method:
        readable_payment_method = PAYMENT_METHODS.get(payment_method, 'Неизвестный метод')
        order_db_id = user_data.get('order_db_id')
        print(f"{order_db_id=}")
        product_price, valute = parse_price_and_valute(user_data.get('product_price')) 
        if PAYMENT_TEST_MODE:
            order_id, payment_link = payment.create_yookassa_order(
                price=product_price,
                order_django_id=order_db_id,
                test_mode=True
            )
            await callback_query.message.answer(
                "Тестовый режим оплаты.\n"
                f"Ваш выбранный способ оплаты: {hbold(readable_payment_method)}\n"
                f"Тестовая ссылка для оплаты: {payment_link}\n\n"
            )
            await callback_query.message.answer(PAYMENT_IS_SUCCESSFUL)
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
        await callback_query.message.answer(ERROR_IN_PAYMENT)

@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """Обработчик предварительного запроса на проверку от Telegram."""
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@payment_router.message()
async def successful_payment(message: types.Message):
    """Обработчик успешной оплаты."""
    THANKS_FOR_PURCASE = load_phrases_from_json_file("THANKS_FOR_PURCASE")
    if message.successful_payment:
        await message.answer(THANKS_FOR_PURCASE)
