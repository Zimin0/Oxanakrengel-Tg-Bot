from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class BotPhrases(models.Model):
    phrases = models.FileField(verbose_name="Файл с фразами в формате .json", upload_to='phrases/')
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def save(self, *args, **kwargs):
        # Фиксированное имя для файла
        filename = 'phrases.json'
        # Путь к новому файлу
        new_path = f'phrases/{filename}'
        # Если файл уже существует, удалить его
        if default_storage.exists(new_path):
            default_storage.delete(new_path)

        # Если загружается новый файл, сначала сохраняем его временно
        if self.phrases and hasattr(self.phrases.file, 'read'):
            content = self.phrases.file.read()

            # Создаем новый ContentFile с фиксированным именем
            self.phrases.save(name=filename, content=ContentFile(content), save=False)

        super(BotPhrases, self).save(*args, **kwargs)

    def __str__(self):
        return f"Фразы бота | {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
