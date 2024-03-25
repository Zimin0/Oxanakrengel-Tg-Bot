from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False

TOKEN = os.getenv("BOT_TOKEN")
DJANGO_URL = os.getenv("DJANGO_URL")
PAYMENT_TOKEN = '123'
