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

async def get_user_setting(setting_slug:str, default=None) -> dict:
    """ Ассинхронно получает объект настройки из django по его slug. """
    user_setting_url = f'{DJANGO_URL}api/user-setting/'
    search_url = f"{user_setting_url}?slug={setting_slug}"
    headers = {"Authorization": f"Token {BOT_AUTH_TOKEN_DRF}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(search_url, headers=headers)
            setting_data = response.json()
            if response.status_code == 200 and len(setting_data) > 0:
                setting_data = setting_data[0]
                print("Настройка найдена:", setting_data)
                return setting_data
            elif response.status_code == 404 or len(setting_data) == 0: 
                print(f"Настройка с указанным {setting_slug} не найдена.")
            else:
                print(f"Ошибка при получении настройки: {response.status_code}")
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к {e}.")
    return default

if __name__ == "__main__":
    setting =  asyncio.run(get_user_setting("PHYSICAL_SHOP_ADDRESS", default='124'))
    print(setting)
