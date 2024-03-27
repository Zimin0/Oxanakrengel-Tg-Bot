from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver

class BotPhrases(models.Model):
    phrases = models.FileField(verbose_name="Файл с фразами в формате .json", upload_to='phrases/')
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def save(self, *args, **kwargs):
        # Удаление предыдущего файла
        if self.pk:
            try:
                old_file = BotPhrases.objects.get(pk=self.pk).phrases
                if old_file.name != self.phrases.name:
                    old_file.delete(save=False)
            except BotPhrases.DoesNotExist:
                pass
        super(BotPhrases, self).save(*args, **kwargs)

    def __str__(self):
        return f"Фразы бота | {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
