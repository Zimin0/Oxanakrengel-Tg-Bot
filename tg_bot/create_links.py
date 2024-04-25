from config import MAX_TELEGRAM_ARG_LENGTH, BOT_TELEGRAM_NAME, SHOP_URL

def get_bot_link_with_arg(product_url:str) -> str:
    """ Создает ссылку на телеграм бота из ссылки на товар в магазине oxanakrengel.com """
    product_name = product_url.split('/')[-1]
    if len(product_name) > MAX_TELEGRAM_ARG_LENGTH:
        raise ValueError("Длина ссылки на товар получается больше максимально доступной в телеграмм!")
    bot_link = f"https://t.me/{BOT_TELEGRAM_NAME}?start={product_name}"
    return bot_link

def get_product_link_in_shop(product_name:str, shop_url:str=SHOP_URL):
    """ Создает ссылку на товар в магазине oxanakrengel.com из названия товара. """
    return f"{shop_url}/{product_name}"

if __name__ == '__main__':
    print(get_bot_link_with_arg(product_url='https://oxanakrengel.com/zhaket-na-molnii'))

# https://t.me/OxanaKrengelShopBot?start=plate-futlyar-s-v-vyrezom
# https://t.me/OxanaKrengelShopBot?start=barkhatnoe-plate-gode-na-korsete-chyornoe
# https://t.me/OxanaKrengelShopBot?start=bryuchnyi-kostyum-iz-grafitovogo-shelka
# https://t.me/OxanaKrengelShopBot?start=bryuchnyi-kostyum-troika-sinii
# https://t.me/OxanaKrengelShopBot?start=zhaket-na-molnii