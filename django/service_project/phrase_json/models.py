from django.db import models
from django.core.exceptions import ValidationError

class BotPhrases(models.Model):
    phrases = models.FileField(verbose_name="Файл с фразами в формате .json")
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def save(self, *args, **kwargs):
        # Проверяем, существует ли уже запись в модели
        if not self.pk and BotPhrases.objects.exists():
            # Если запись существует, вызываем исключение
            raise ValidationError('Невозможно создать более одной записи BotPhrases.')
        return super(BotPhrases, self).save(*args, **kwargs)

    def __str__(self):
        return f"Фразы бота | {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
