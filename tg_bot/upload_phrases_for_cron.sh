#!/bin/bash

# Указываем путь, где будет создано виртуальное окружение
VENV_PATH="./venv"

# Создаем виртуальное окружение, если оно еще не создано
if [ ! -d "$VENV_PATH" ]; then
    echo "Создание виртуального окружения в $VENV_PATH..."
    python3 -m venv $VENV_PATH
else
    echo "Виртуальное окружение уже существует."
fi

# Активируем виртуальное окружение
echo "Активация виртуального окружения..."
source $VENV_PATH/bin/activate

# Устанавливаем необходимые пакеты
echo "Установка необходимых пакетов: httpx, asyncio, pathlib..."
pip install python-dotenv httpx asyncio pathlib

# Выполняем скрипт
echo "Выполнение скрипта /bot/httpx_requests/json_file.py..."
python /bot/httpx_requests/json_file.py

# Деактивация виртуального окружения (необязательно, если скрипт завершает работу)
echo "Деактивация виртуального окружения..."
deactivate
