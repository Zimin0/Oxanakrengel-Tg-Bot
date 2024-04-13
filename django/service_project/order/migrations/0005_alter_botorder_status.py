# Generated by Django 4.2.1 on 2024-04-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_botorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botorder',
            name='status',
            field=models.CharField(choices=[('waiting_for_payment', 'Ожидает оплаты'), ('was_paid', 'Оплачен'), ('canceled', 'Отменен'), ('delivery_in_progress', 'В процессе доставки'), ('finished', 'Завершен'), ('returned', 'Возврат')], max_length=60, verbose_name='Статус заказа'),
        ),
    ]
