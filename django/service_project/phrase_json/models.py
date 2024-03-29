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

        # Удалить старый файл, если загружен новый
        if self.phrases:
            # Полный путь к старому файлу
            old_path = self.phrases.path
            # Проверяем, совпадает ли путь нового файла со старым
            if not old_path.endswith(filename):
                # Если файл уже существует, удаляем его
                if default_storage.exists(new_path):
                    default_storage.delete(new_path)
                # Считываем содержимое нового файла
                content = self.phrases.read()
                # Заменяем файл
                self.phrases.save(name=filename, content=ContentFile(content), save=False)
        else:
            # Если файл не прикреплен, не делаем ничего
            if not default_storage.exists(new_path):
                raise ValueError("Файл phrases.json отсутствует.")

        super(BotPhrases, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Файл фраз бота"
        verbose_name_plural = "Файлы фраз бота"

    def __str__(self):
        return f"Фразы бота | {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
