MAX_TELEGRAM_ARG_LENGTH = 64
BOT_NAME = 'OxanaKrengelShopBot'

def get_bot_link_with_arg(product_url:str) -> str:
    """ Создает ссылку на телеграм бота из ссылки на товар в магазине oxanakrengel.com """
    product_name = product_url.split('/')[-1]
    if len(product_name) > MAX_TELEGRAM_ARG_LENGTH:
        raise ValueError("Длина ссылки на товар получается больше максимально доступной в телеграмм!")
    bot_link = f"https://t.me/{BOT_NAME}?start={product_name}"
    return bot_link

def get_product_link_in_shop(product_name:str):
    """ Создает ссылку на товар в магазине oxanakrengel.com из названия товара. """
    return f"https://oxanakrengel.com/{product_name}"

print(get_bot_link_with_arg(product_url='https://oxanakrengel.com/plate-futlyar-s-vyrezom-lodochkoi-i-manzhetami-krasnoe'))