# Generated by Django 4.2.1 on 2024-03-25 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supportrequest',
            options={'ordering': ['-creation_date'], 'verbose_name': 'Запрос в поддержку', 'verbose_name_plural': 'Запросы в поддержку'},
        ),
        migrations.AlterField(
            model_name='supportrequest',
            name='user',
            field=models.CharField(max_length=100, verbose_name='Идентификатор пользователя telegram'),
        ),
    ]
