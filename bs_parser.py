import requests
from bs4 import BeautifulSoup
import time
import json  # Импорт модуля для работы с JSON

# Декоратор для измерения времени выполнения функции
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} выполнена за {round(end_time - start_time, 3)} секунд.")
        return result
    return wrapper

@time_decorator
def get_html(url):
    """Получение HTML-контента по URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f'Ошибка при загрузке страницы, код ответа HTTP: {response.status_code}')
        return None

@time_decorator
def parse_html(html_content):
    """Парсинг HTML и извлечение данных."""
    soup = BeautifulSoup(html_content, 'html.parser')
    product = {
        "title": soup.find('h2', class_='flex-box').text.strip(),
        "price": soup.find('div', class_='cart-info__price').text.strip(),
        "sizes": [label.text.strip() for label in soup.find_all('label', class_='cart-info__btn-size radio')],
        "description": soup.find('div', class_='cart-info__discription').find('p').text.strip() if soup.find('div', class_='cart-info__discription').find('p') else "Описание отсутствует",
        "image_urls": [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    }
    return product

def save_to_json(data, filename="product_info.json"):
    """Сохранение данных о продукте в JSON файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    url = "https://oxanakrengel.com/tvidovyi-kostyum-goluboi"
    html_content = get_html(url)
    if html_content:
        product_info = parse_html(html_content)
        save_to_json(product_info)
        print(f'Информация о продукте сохранена в файл {product_info["title"]}.json')

if __name__ == "__main__":
    main()
