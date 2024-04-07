#!/bin/bash
crontab -l > mycron

# Добавить задачу cron для очистки директории
echo "0 0 * * * /bot/clear_products_json.sh" >> mycron

# Добавить задачу cron для запуска скрипта Python каждую минуту
echo "* * * * * python /bot/httpx_requests/json_file.py" >> mycron

crontab mycron
rm mycron
