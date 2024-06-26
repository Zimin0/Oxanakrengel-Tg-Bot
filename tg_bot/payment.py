import datetime
import pytz
from yookassa import Configuration, Payment
import uuid
from dotenv import load_dotenv
import os
from config import BOT_TELEGRAM_NAME, PAYMENT_TEST_MODE

load_dotenv()

if PAYMENT_TEST_MODE:
    YOOKASSA_ACCOUNT_ID_sample = 'YOOKASSA_ACCOUNT_ID'
    YOOKASSA_SECRET_KEY_sample = 'YOOKASSA_SECRET_KEY' 
else:
    YOOKASSA_ACCOUNT_ID_sample = 'YOOKASSA_PRODUCTION_ACCOUNT_ID'
    YOOKASSA_SECRET_KEY_sample = 'YOOKASSA_PRODUCTION_SECRET_KEY' 

Configuration.account_id = os.getenv(YOOKASSA_ACCOUNT_ID_sample)
Configuration.secret_key = os.getenv(YOOKASSA_SECRET_KEY_sample) 

class Custom_Payment():
    @property
    def return_url(self):
        return f'https://t.me/{BOT_TELEGRAM_NAME}'

    @staticmethod
    def __create_date() -> str:
        """ Генерирует дату в формате 2018-07-18T10:51:18.139Z """
        current_time = datetime.datetime.now(pytz.utc)
        formatted_date = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return formatted_date

    @staticmethod
    def __create_description(order_django_id:int, price:float, currency:str='rub') -> str:
        """ * order_django_id - id из базы данных django. """
        return f"Заказ №{order_django_id} на сумму {price} {currency}"

    def create_yookassa_order(self, price:float, order_django_id:int, test_mode:bool=False):
        """
        * price - суммарная цена заказа (float).
        * order_django_id - django pk из базы данных (int).
        * test_mode - тестирование или нет
        """
        payment = Payment.create({
            "id": str(uuid.uuid4()),
            'status': "pending ",
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "description": Custom_Payment.__create_description(order_django_id, price),
            "test": test_mode,
            "created_at": Custom_Payment.__create_date(),
            "confirmation": {
                "type": "redirect",
                "return_url": self.return_url
            },
            "capture": True,
            "metadata": {
                "order_django_id":order_django_id
            }
            
        }, uuid.uuid4())
        return payment.id, payment.confirmation.confirmation_url

if __name__ == "__main__":
    payment = Custom_Payment()
    print(payment.create_yookassa_order(1.0, order_django_id=10, test_mode=True))

