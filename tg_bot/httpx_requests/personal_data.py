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


async def get_or_create_personal_data(telegram_user_id: str, name: str, surname: str, address: str, email: str, phone_number: str) -> int:
    """Asynchronously retrieves or creates Telegram user's data. Returns the record id."""
    personal_data_url = f'{DJANGO_URL}api/personaldata/'
    search_url = f"{personal_data_url}?telegram_user_id={telegram_user_id}"
    headers = {"Authorization": f"Token {BOT_AUTH_TOKEN_DRF}"}
    
    new_personal_data = {
        "telegram_user_id": telegram_user_id,
        "name": name,
        "surname": surname,
        "address": address,
        "email": email,
        "phone_number": phone_number
    }

    print(f"Данные, которые хотим занести в БД: {new_personal_data=}")

    async with httpx.AsyncClient() as client:
        try:
            # Попытка найти существующие пользовательские данные
            search_response = await client.get(search_url, headers=headers)
            if search_response.status_code == 200:
                search_data = search_response.json()
                # Проверьте, существует ли пользователь уже
                if search_data:
                    user_id = search_data[0]['id']  # Предполагая, что API возвращает список
                    update_url = f"{personal_data_url}{user_id}/"
                    # Обновите существующие данные пользователя
                    update_response = await client.patch(update_url, json=new_personal_data)
                    print(f"{update_response=} {update_response.status_code=} {update_response.json()}")
                    if update_response.status_code in (200, 202):  # 202 Принято к обновлению
                        updated_data = update_response.json()
                        print("Updated existing PersonalData record:", updated_data)
                        return updated_data['id']
                    else:
                        print("Error updating PersonalData")
                        print("Status code:", update_response.status_code)
                        print("Error:", update_response.text)
                        return None
                else:
                    # Если пользователь не существует, создайте новую запись
                    create_response = await client.post(personal_data_url, json=new_personal_data)
                    if create_response.status_code in (200, 201):
                        data = create_response.json()
                        print("Created new PersonalData record:", data)
                        return data['id']
                    else:
                        print("Error creating PersonalData")
                        print("Status code:", create_response.status_code)
                        print("Error:", create_response.text)
                        return None
        except httpx.RequestError as e:
            print(f"Error during request to {e.request.url!r}.")
            return None

if __name__ == '__main__':
    telegram_user_id = '@test1'
    name = "test_name"
    surname = "test_surname"
    address = "test_address"
    email = "test@gmail.com"
    phone_number = "7999999999"
    asyncio.run(get_or_create_personal_data(telegram_user_id, name, surname, address, email, phone_number))
