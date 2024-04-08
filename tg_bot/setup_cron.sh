#!/bin/bash
crontab -l > mycron
# Добавить задачу cron для очистки директории
echo "0 0 * * * /bin/bash /bot/clear_products_json.sh" >> mycron
# Добавить задачу cron для запуска скрипта Python каждую минуту
echo "* * * * * /bin/bash /bot/upload_phrases_for_cron.sh" >> mycron
crontab mycron
rm mycron
