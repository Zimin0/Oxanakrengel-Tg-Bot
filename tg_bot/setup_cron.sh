#!/bin/bash
crontab -l > mycron
# Добавить задачу cron для очистки директории
echo "* * * * * rm -rf /bot/products_json/*" >> mycron
# Добавить задачу cron для запуска скрипта Python каждую минуту
echo "* * * * * /usr/local/bin/python /bot/httpx_requests/json_file.py" >> mycron
echo ""
crontab mycron
rm mycron
