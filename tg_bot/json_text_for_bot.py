import json
from config import PHRASES_FILE_NAME

def load_phrases_from_json_file(*slugs):
    """
    Загружает и возвращает фразы или вложенные словари для ответа ботом из json файла.
    Если передан один ключ, возвращает строку.
    Если передано несколько ключей, возвращает список соответствующих значений.
    """
    file_path = PHRASES_FILE_NAME
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            phrases = json.load(file)
            results = [phrases.get(slug) for slug in slugs if slug in phrases]
            
            if len(slugs) != len(results):
                raise ValueError("Одна или несколько фраз для указанных ключей не найдены.")
            
            # Если аргумент был только один, возвращаем строку, иначе - список
            return results[0] if len(slugs) == 1 else results
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        raise ValueError("Ошибка при декодировании JSON файла.")
