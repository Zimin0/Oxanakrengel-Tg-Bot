from django.db import models

class Setting(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название настройки", help_text="Можно поставить любое")
    slug = models.SlugField(max_length=30, verbose_name="Слаг. Не трогать!", help_text="Используется в коде. Нельзя изменять!", blank=False)
    value = models.CharField(max_length=400, verbose_name="Значение", help_text="Если это номер телефона, то: +79315663388", blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return f'{self.name}'