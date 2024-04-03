#!/bin/bash

# Добавить задачу cron для очистки директории
echo "0 0 * * * /path/to/clear_products_json.sh" > /etc/cron.d/telegram_bot_cron

# Добавить задачу cron для запуска скрипта Python каждую минуту
echo "* * * * * python /path/to/httpx_requests/json_file.py" >> /etc/cron.d/telegram_bot_cron

# Права на файл для cron
chmod 0644 /etc/cron.d/telegram_bot_cron

# Применить изменения cron
crontab /etc/cron.d/telegram_bot_cron

# Запустить cron в фоне
cron -f
