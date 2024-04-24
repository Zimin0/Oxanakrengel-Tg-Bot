from dotenv import load_dotenv
import os

load_dotenv()

PAYMENT_TEST_MODE = True

TOKEN = os.getenv("BOT_TOKEN")
DJANGO_URL = os.getenv("DJANGO_URL")