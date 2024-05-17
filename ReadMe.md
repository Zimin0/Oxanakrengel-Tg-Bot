## Бот для продажи товаров из магазина oxanakrengel.com
### Использование
1) [domain]/admin - админка
2) [domain]/link - тут нужно вставить ссылку на товар, например https://oxanakrengel.com/bryuchnyi-kostyum-grani-goluboi - получим ссылку на товар для покупке в боте для тг канала https://t.me/oxanakrengel, откуда пользователи будут переходить в бота.

### Технологии и библиотеки
* Django
* Django Rest Framework
* Aiogram: основа ТГ бота.
* httpx + asyncio: запросы к API от бота.
* Платежная система: Yookassa
* nginx: веб-сервер и обратный прокси.
* cron + CronTab: обновление ssl + подкачка файла с фразами бота из API.
* HTML/CSS/JS
* Docker-compose
* bash: добавление задач в cron

### Архитектура
Микросервисная архитектура, контейнеры: 
* Django с API эндпоинтами (DRF), админкой и страницами для генерации ссылок.
* Бот на aiogram
* PostgreSQL
* Nginx + ssl на хосте

* Проект работает только с ценой в рублях 24.04.2024
