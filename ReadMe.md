## Бот для продажи товаров из магазина oxanakrengel.com
### Использование
1) [domain]/admin - админка
2) [domain]/link - тут нужно вставить ссылку на товар, например https://oxanakrengel.com/bryuchnyi-kostyum-grani-goluboi - получим ссылку на товар для покупке в боте для тг канала https://t.me/oxanakrengel, откуда пользователи будут переходить в бота.

### Технологии и библиотеки
* Django
* Django Rest Framework + Token AUTH
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

### Скриншоты

* Вывод информации о товаре

![image](https://github.com/Zimin0/Oxanakrengel-Tg-Bot/assets/67171139/bff6fcc5-afea-44ab-a805-d47949f324f8)


![image](https://github.com/Zimin0/Oxanakrengel-Tg-Bot/assets/67171139/8d2692ea-e44d-4147-b5df-7f0d2f1c010f)

![image](https://github.com/Zimin0/Oxanakrengel-Tg-Bot/assets/67171139/0c05d525-b41f-4007-bbee-44c7a7ecb478)


* Админка

![image](https://github.com/Zimin0/Oxanakrengel-Tg-Bot/assets/67171139/000aacf3-1785-423b-b39e-b0fe3bc4b9a5)

* Генерация ссылок

![image](https://github.com/Zimin0/Oxanakrengel-Tg-Bot/assets/67171139/ca03a3f5-6593-4342-bb88-2370223159ca)


* Проект работает только с ценой в рублях 24.04.2024
