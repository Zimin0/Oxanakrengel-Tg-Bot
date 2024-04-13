import httpx
import asyncio
import sys

# Необходимо добавить импорт для Path, если он не был добавлен ранее
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from config import DJANGO_URL
async def fetch_bot_phrases():
    """Асинхронно запрашивает и сохраняет файл с фразами для бота."""
    phrases_url = f'{DJANGO_URL}api/bot-phrases/'  # URL для получения фраз бота
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(phrases_url)
            if response.status_code == 200:
                # ответ от сервера - это строка в формате JSON
                data = response.json()
                # Определяем путь к файлу на уровень выше от текущей директории скрипта
                file_path = Path(__file__).resolve().parent.parent / 'phrases.json'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
                print(f"Файл с фразами успешно сохранен в {file_path}")
            else:
                print("Ошибка при получении файла с фразами")
                print("Статус код:", response.status_code)
                print("Ошибка:", response.text)
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e.request.url!r}.")

if __name__ == '__main__':
    asyncio.run(fetch_bot_phrases())
