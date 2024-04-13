from django.db import models
from django.utils import timezone

class PersonalData(models.Model):
    telegram_user_id = models.CharField(verbose_name="Идентификатор пользователя telegram", max_length=100, blank=False, unique=True)
    name = models.CharField(verbose_name="Имя", max_length=80, blank=False)
    surname = models.CharField(verbose_name="Фамилия", max_length=80, blank=False)
    address = models.TextField(verbose_name="Адрес", blank=True, null=True)
    email = models.EmailField(verbose_name="Почта", blank=False)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=20, blank=False)

    def __str__(self):
        return f"Пользователь - {self.telegram_user_id}"
    
    class Meta:
        verbose_name = "Данные пользователя telegram"
        verbose_name_plural = "Данные пользователя telegram"

class BotOrder(models.Model):
    SHIPPING_METHODS = (
        ("delivery_moscow", "Доставка курьером по Москве"),
        ("delivery_russia", "Доставка курьером по России"),
        ("delivery_pickup", "Самовывоз")
    )
    PAYMENT_METHODS = (
        ("card_ru", "Карта РФ "),
        ("paypal", "PayPal"),
    )
    STATUSES = (
        ('waiting_for_payment', 'Ожидает оплаты'),
        ('was_paid', 'Оплачен'),
        ('canceled', 'Отменен'),
        ('delivery_in_progress', 'В процессе доставки'),
        ('finished', 'Завершен'),
        ('returned', 'Возврат')
    ) 
    personal_data = models.ForeignKey(PersonalData, on_delete=models.PROTECT, related_name="orders")
    product_link = models.CharField(verbose_name="Ссылка на товар в магазине", max_length=300, blank=False)
    size = models.IntegerField(verbose_name="Размер одежды", blank=False)
    shipping_method = models.CharField(verbose_name="Метод доставки", max_length=50, choices=SHIPPING_METHODS)
    payment_method = models.CharField(verbose_name="Метод оплаты", max_length=50, choices=PAYMENT_METHODS)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=10, blank=False)
    payment_id = models.CharField(verbose_name="ID заказа из платежной системы", max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(verbose_name="Оплачен", default=False)
    is_real_order = models.BooleanField(verbose_name="Настоящий", default=False)
    status = models.CharField(verbose_name="Статус заказа", max_length=60, choices=STATUSES)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"Заказ №{self.id}"

    class Meta:
        verbose_name = "Заказ в telegram боте"
        verbose_name_plural = "Заказы в telegram боте"
        ordering = ['-creation_date']