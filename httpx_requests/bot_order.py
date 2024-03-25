import httpx
import asyncio
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL

async def create_bot_order(personal_data_id: int, product_link: str, size: int, shipping_method: str, payment_method: str, price: float, status: str):
    """ Асинхронно создает заказ с товаром. """
    bot_order_url = f'{DJANGO_URL}api/botorder/'
    new_bot_order = {
        "personal_data": personal_data_id,
        "product_link": product_link,
        "size": size,
        "shipping_method": shipping_method,
        "payment_method": payment_method,
        "price": price,
        "status": status
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(bot_order_url, json=new_bot_order)
            if response.status_code in (200, 201):
                print("Создана новая запись BotOrder:", response.json())
            else:
                print("Ошибка при создании BotOrder")
                print("Статус код:", response.status_code)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")

if __name__ == '__main__':
    personal_data = 1
    product_link = 'https://oxanakrengel.com/zhaket-na-molnii'
    size = 48
    shipping_method = 'delivery_russia'
    payment_method = 'paypal'
    price = 12000.00
    status = 'waiting_for_payment'
    asyncio.run(create_bot_order(personal_data, product_link, size, shipping_method, payment_method, price, status))
