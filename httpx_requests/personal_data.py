import httpx
import asyncio
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL


async def create_personal_data(telegram_user_id: str, name: str, surname: str, address: str, email: str, phone_number: str):
    """ Асинхронно сохраняет данные о пользователе telegram. """
    personal_data_url = f'{DJANGO_URL}api/personaldata/'

    new_personal_data = {
        "telegram_user_id": telegram_user_id,
        "name": name,
        "surname": surname,
        "address": address,
        "email": email,
        "phone_number": phone_number
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(personal_data_url, json=new_personal_data)
            if response.status_code in (200, 201):
                print("Создана новая запись PersonalData:", response.json())
            else:
                print("Ошибка при создании PersonalData")
                print("Статус код:", response.status_code)
                print("Ошибка:", response.text)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")

if __name__ == '__main__':
    telegram_user_id = '@test1'
    name = "test_name"
    surname = "test_surname"
    address = "test_address"
    email = "test@gmail.com"
    phone_number = "7999999999"
    asyncio.run(create_personal_data(telegram_user_id, name, surname, address, email, phone_number))
