from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from states import PaymentState
from payment import Custom_Payment
from config import PAYMENT_TEST_MODE
from json_text_for_bot import load_phrases_from_json_file
from utils import is_payment_callback, parse_price_and_valute, is_check_payment_callback
from keyboards import get_final_pay_keyboard
from httpx_requests.get_order_object import get_order_by_id

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
        order_id, payment_link = payment.create_yookassa_order(
            price=product_price,
            order_django_id=order_db_id,
            test_mode=PAYMENT_TEST_MODE
        )
        label = "Тестовый режим оплаты ⚙️\n" if PAYMENT_TEST_MODE else ""
        await callback_query.message.answer(
            label +
            f"Ваш выбранный способ оплаты: {hbold(readable_payment_method)}\n" +
            f"Оплатите заказ по кнопке ниже ⬇️", 
            reply_markup=get_final_pay_keyboard(payment_link)
        )
    else:
        await callback_query.message.answer(ERROR_IN_PAYMENT)

@payment_router.callback_query(is_check_payment_callback)
async def process_final_payment(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик нажатия на кнопку "Я оплатил" """

    PAYMENT_IS_SUCCESSFUL, STILL_NO_PAYMENT = load_phrases_from_json_file("PAYMENT_IS_SUCCESSFUL", "STILL_NO_PAYMENT")
    # оправляет запрос на сервер #
    user_data = await state.get_data()
    django_order_id = user_data.get("order_db_id", None)
    if not django_order_id:
        raise KeyError("order_db_id не найден в сессии!")
    
    order_object = await get_order_by_id(django_order_id)
    is_paid = order_object['is_paid']
    order_yookassa_id = order_object['payment_id'] 
    if is_paid:
        await callback_query.message.answer(f"{PAYMENT_IS_SUCCESSFUL} \n<b>ID вашего заказ</b>: {order_yookassa_id}")
    else:
        await callback_query.message.answer(STILL_NO_PAYMENT)

# @payment_router.pre_checkout_query()
# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
#     """Обработчик предварительного запроса на проверку от Telegram."""
#     await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
