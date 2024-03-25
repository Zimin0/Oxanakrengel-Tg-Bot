import httpx

import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL

def create_support_request(user_id: int, text: str, status: str = "in_progress"):
    support_request_url = f'{DJANGO_URL}api/supportrequest/'
    new_support_request_data = {
        "user": user_id,
        "text": text,
        "status": status
    }
    try:
        response = httpx.post(support_request_url, json=new_support_request_data)
        if response.status_code in (200, 201):
            created_request = response.json()
            print("Создан новый SupportRequest:", created_request)
        else:
            print("Ошибка при создании SupportRequest")
            print("Статус код:", response.status_code)
    except httpx.RequestError as e:
        print(f"Ошибка при запросе к {e.request.url!r}.")

if __name__ == '__main__':
    user_id = 1
    text = "Это тестовый запрос в поддержку"
    create_support_request(user_id, text)
