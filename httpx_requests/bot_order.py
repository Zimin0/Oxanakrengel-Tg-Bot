import httpx
import asyncio
import sys
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

BOT_AUTH_TOKEN_DRF = os.getenv('BOT_AUTH_TOKEN_DRF')

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL

async def create_bot_order(personal_data_id: int, product_link: str, size: int, shipping_method: str, payment_method: str, price: float, status: str, is_real_order:bool) -> str:
    """ Асинхронно создает заказ с товаром. Воззвращает id из базы данных."""
    bot_order_url = f'{DJANGO_URL}api/botorder/'
    new_bot_order = {
        "personal_data": personal_data_id,
        "product_link": product_link,
        "size": size,
        "shipping_method": shipping_method,
        "payment_method": payment_method,
        "price": price,
        "status": status,
        "is_real_order": is_real_order
    }
    headers = {"Authorization": f"Token {BOT_AUTH_TOKEN_DRF}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(bot_order_url, json=new_bot_order, headers=headers)
            if response.status_code in (200, 201):
                response_json = response.json()
                print("Создана новая запись BotOrder:", response_json)
                return str(response_json['id'])
            else:
                print("Ошибка при создании BotOrder")
                print("Статус код:", response.status_code)
                print("Ошибка:", response.text)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")
    return None

if __name__ == '__main__':
    personal_data = 1
    product_link = 'https://oxanakrengel.com/zhaket-na-molnii'
    size = 48
    shipping_method = 'DELIVERY_RUSSIA'
    payment_method = 'paypal'
    price = 12000.00
    status = 'waiting_for_payment'
    is_real_order = False
    asyncio.run(create_bot_order(personal_data, product_link, size, shipping_method, payment_method, price, status, is_real_order))
