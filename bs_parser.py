import requests
from bs4 import BeautifulSoup
from typing import Callable, Any, Dict, Optional
import time
import hashlib
import json
import os

class WebPageParser:
    def __init__(self, debug: bool = False, folder: str = '', can_upload_from_file: bool = False) -> None:
        """ 
        folder - папка для сохранения файлов 
        can_upload_from_file - можно ли подтягивать изменения из файла или нужно обязательно скачивать с сайта
        """
        self.debug = debug
        self.folder = folder 
        self.can_upload_from_file = can_upload_from_file
        os.makedirs(self.folder, exist_ok=True)
    
    @staticmethod
    def time_decorator(func: Callable) -> Callable:
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            start_time = time.time() if self.debug else None
            result: Any = func(self, *args, **kwargs)
            if self.debug:
                end_time: float = time.time()
                print(f"{func.__name__} выполнена за {round(end_time - start_time, 3)} секунд.")
            return result
        return wrapper

    @time_decorator
    def __get_html(self, url: str) -> str:
        """Получение HTML-контента по URL."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f'Ошибка при загрузке страницы, код ответа HTTP: {response.status_code}')
            return None

    @time_decorator
    def __parse_html(self, html_content: str, url:str) -> Dict[str, Any]:
        """Парсинг HTML и извлечение данных."""
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('h2', class_='flex-box').text.strip()
        unique_id = hashlib.md5(title.encode('utf-8')).hexdigest()
        image_urls_set = set(img['src'] for img in soup.find_all('img') if 'src' in img.attrs and '1360x2040' in img['src'])
        product = {
            "id": unique_id,
            "title": title,
            "price": soup.find('div', class_='cart-info__price').text.strip(),
            "sizes": [label.text.strip() for label in soup.find_all('label', class_='cart-info__btn-size radio')],
            "description": soup.find('div', class_='cart-info__discription').find('p').text.strip() if soup.find('div', class_='cart-info__discription').find('p') else "Описание отсутствует",
            "image_urls": list(image_urls_set),
            "url": url
        }
        return product

    def __save_to_json(self, data, filepath) -> None:
        """Сохранение данных о продукте в JSON файл."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if self.debug: print(f'Информация о продукте сохранена в файл {filepath}.')

    def run(self, url: str, save_to_file: bool = False) -> tuple[str, Optional[str]]:
        # Создание уникального ID на основе URL для проверки существования файла
        unique_id = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = f"product_info_{unique_id}.json"
        filepath = os.path.join(self.folder, filename)

        # Проверка наличия файла с данными о товаре
        if os.path.exists(filepath) and self.can_upload_from_file:
            if self.debug: print(f'Информация о продукте загружается из файла {filepath}.')
            with open(filepath, 'r', encoding='utf-8') as f:
                product_info = json.load(f)
                return filepath, json.dumps(product_info, ensure_ascii=False, indent=4)

        # Если файла нет, производим парсинг и сохраняем результаты
        html_content = self.__get_html(url)
        if html_content:
            product_info = self.__parse_html(html_content, url)
            if save_to_file:
                self.__save_to_json(product_info, filepath)
            return filepath, json.dumps(product_info, ensure_ascii=False, indent=4)

        return filepath, None

if __name__ == "__main__":
    parser = WebPageParser(debug=True, folder='products_json', can_upload_from_file=True)
    filename, json_data = parser.run("https://oxanakrengel.com/plate-futlyar-s-vyrezom-lodochkoi-i-manzhetami-krasnoe", save_to_file=False)