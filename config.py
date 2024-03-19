from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True

TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_TOKEN = '123'

PHYSICAL_SHOP_ADDRESS = "Москва, ул. Примерная, д. 10, 3 этаж"
PAYMENT_METHODS = {
    'card_ru': 'Карта РФ 💵',
    'paypal': 'PayPal 📘',
}
SHIPPING_METHODS = {
    'delivery_moscow': 'Доставка курьером по Москве 🚚',
    'delivery_russia': 'Доставка курьером по России 🛫',
    'delivery_pickup': 'Самовывоз 🏃🏼'
}
