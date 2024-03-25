# Generated by Django 4.2.1 on 2024-03-25 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0002_alter_botorder_creation_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Запрос')),
                ('status', models.CharField(choices=[('in_progress', 'Ожидает ответа'), ('finished', 'Завершена')], max_length=60, verbose_name='Статус заявки')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='support_requests', to='order.personaldata')),
            ],
            options={
                'verbose_name': 'Запрос поддержки',
                'verbose_name_plural': 'Запросы поддержки',
                'ordering': ['-creation_date'],
            },
        ),
    ]
