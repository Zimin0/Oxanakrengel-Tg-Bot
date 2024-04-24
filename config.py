from dotenv import load_dotenv
import os

load_dotenv()

PAYMENT_TEST_MODE = True

MAX_TELEGRAM_ARG_LENGTH = 64 # максимальная длина агрумента, передаваемого в команду start=
BOT_TELEGRAM_NAME = 'OxanaKrengelShopBot'
SHOP_URL = 'https://oxanakrengel.com'
PHRASES_FILE_NAME = 'phrases.json'

TOKEN = os.getenv("BOT_TOKEN")
DJANGO_URL = os.getenv("DJANGO_URL")