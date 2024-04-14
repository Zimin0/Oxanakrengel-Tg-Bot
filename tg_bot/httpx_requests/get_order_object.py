import httpx
import asyncio
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL

async def get_order_by_id(order_id: int) -> dict:
    """Асинхронно получает объект заказа по его id."""
    bot_order_url = f'{DJANGO_URL}api/botorder/{order_id}/'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(bot_order_url)
            if response.status_code == 200:
                order_data = response.json()
                print("Заказ найден:", order_data)
                return order_data
            elif response.status_code == 404:
                print("Заказ с указанным id не найден.")
            else:
                print("Ошибка при получении заказа.")
                print("Статус код:", response.status_code)
                print("Ошибка:", response.text)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")
    return None

if __name__ == "__main__":
    order_id = 24
    order =  asyncio.run(get_order_by_id(order_id))
    if order:
        print("Обработка полученного заказа:", order)
    else:
        print("Заказ не найден.")


    