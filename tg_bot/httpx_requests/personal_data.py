import httpx
import asyncio
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL


async def get_or_create_personal_data(telegram_user_id: str, name: str, surname: str, address: str, email: str, phone_number: str) -> int:
    """Asynchronously retrieves or creates Telegram user's data. Returns the record id."""
    personal_data_url = f'{DJANGO_URL}api/personaldata/'
    search_url = f"{personal_data_url}?search={telegram_user_id}"
    
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
            # Попытка найти существующие пользовательские данные
            search_response = await client.get(search_url)
            if search_response.status_code == 200:
                search_data = search_response.json()
                # Проверьте, существует ли пользователь уже
                if search_data:
                    user_id = search_data[0]['id']  # Предполагая, что API возвращает список
                    update_url = f"{personal_data_url}{user_id}/"
                    # Обновите существующие данные пользователя
                    update_response = await client.patch(update_url, json=new_personal_data)
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
