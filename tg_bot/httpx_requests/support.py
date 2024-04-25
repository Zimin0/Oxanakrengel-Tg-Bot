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

async def create_support_request(user_id: int, text: str, status: str = "in_progress"):
    """ Асинхронно создает запрос в тех. поддержку. """
    support_request_url = f'{DJANGO_URL}api/supportrequest/'
    new_support_request_data = {
        "user": user_id,
        "text": text,
        "status": status
    }
    headers = {"Authorization": f"Token {BOT_AUTH_TOKEN_DRF}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(support_request_url, json=new_support_request_data, headers=headers)
            if response.status_code in (200, 201):
                created_request = response.json()
                print("Создан новый SupportRequest:", created_request)
            else:
                print("Ошибка при создании SupportRequest")
                print("Статус код:", response.status_code)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")

if __name__ == '__main__':
    user_id = "@Zimin0"
    text = "Это тестовый запрос в поддержку2"
    asyncio.run(create_support_request(user_id, text))
