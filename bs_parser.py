import requests
from bs4 import BeautifulSoup
from typing import Callable, Any, Dict, Optional
import time
import hashlib
import json

class WebPageParser:
    def __init__(self, debug: bool = False) -> None:
        self.debug: bool = debug
        
    def time_decorator(func: Callable) -> Callable:
        def wrapper(self: 'WebPageParser', *args: Any, **kwargs: Any) -> Any:
            start_time: Optional[float] = time.time() if self.debug else None
            result: Any = func(self, *args, **kwargs)
            if self.debug:
                end_time: float = time.time()
                print(f"{func.__name__} выполнена за {round(end_time - start_time, 3)} секунд.")
            return result
        return wrapper

    @time_decorator
    def get_html(self, url: str) -> Optional[str]:
        """Получение HTML-контента по URL."""
        response: requests.Response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f'Ошибка при загрузке страницы, код ответа HTTP: {response.status_code}')
            return None

    @time_decorator
    def parse_html(self, html_content: str) -> Dict[str, Any]:
        """Парсинг HTML и извлечение данных."""
        soup: BeautifulSoup = BeautifulSoup(html_content, 'html.parser')
        title: str = soup.find('h2', class_='flex-box').text.strip()
        unique_id: str = hashlib.md5(title.encode('utf-8')).hexdigest()
        product: Dict[str, Any] = {
            "id": unique_id,
            "title": title,
            "price": soup.find('div', class_='cart-info__price').text.strip(),
            "sizes": [label.text.strip() for label in soup.find_all('label', class_='cart-info__btn-size radio')],
            "description": soup.find('div', class_='cart-info__discription').find('p').text.strip() if soup.find('div', class_='cart-info__discription').find('p') else "Описание отсутствует",
            "image_urls": [img['src'] for img in soup.find_all('img') if 'src' in img.attrs and '1360x2040.jpg' in img['src']]
        }
        return product

    def save_to_json(self, data: Dict[str, Any]) -> None:
        """Сохранение данных о продукте в JSON файл с уникальным именем."""
        filename: str = f"product_info_{data['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if self.debug: print(f'Информация о продукте "{data["title"]}" сохранена в файл {filename}.')

    def run(self, url: str, save_to_file: bool = False) -> str:
        html_content: Optional[str] = self.get_html(url)
        if html_content:
            product_info: Dict[str, Any] = self.parse_html(html_content)
            if save_to_file:
                self.save_to_json(product_info)
            return json.dumps(product_info, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = WebPageParser(debug=True)
    json_data = parser.run("https://oxanakrengel.com/tvidovyi-kostyum-goluboi", save_to_file=True)
    print(json_data)
