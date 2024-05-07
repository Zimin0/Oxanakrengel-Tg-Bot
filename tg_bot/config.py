from dotenv import load_dotenv
import os

load_dotenv()

PAYMENT_TEST_MODE = False
DISABLE_VALIDATION = False

MAX_TELEGRAM_ARG_LENGTH = 64 # максимальная длина агрумента, передаваемого в команду start=
BOT_TELEGRAM_NAME = 'OxanaKrengelShopBot'
SHOP_URL = 'https://oxanakrengel.com'
PHRASES_FILE_NAME = 'phrases.json'

TOKEN = os.getenv("BOT_TOKEN")
DJANGO_URL = os.getenv("DJANGO_URL")

debug_data_for_personal = {
    "telegram_user_id": "@TestUser",
    "name": "TestName",
    "surname": "TestSurname",
    "address": "123 Test St, Test City, Test United Country",
    "email": "test@example.com",
    "phone_number": "+79313664444"
}

debug_data_for_order = {
    "product_link": "http://example.com/product",
    "size": 45,
    "shipping_method": "delivery_moscow",
    "payment_method": "card_ru",
    "price": 100.0,
    "status": 'waiting_for_payment',
    "is_real_order": False
}