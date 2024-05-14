from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseNotFound, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import os

class BotPhrases(models.Model):
    phrases = models.FileField(verbose_name="Файл с фразами в формате .json", upload_to='phrases/')
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    def save(self, *args, **kwargs):
        # Фиксированное имя для файла
        filename = 'phrases.json'
        # Путь к новому файлу
        new_path = os.path.join('phrases', filename)

        # Удалить предыдущий файл, если он существует
        if default_storage.exists(new_path):
            default_storage.delete(new_path)

        # Если прикреплен новый файл
        if self.phrases:
            # Считываем содержимое нового файла
            content = self.phrases.read()
            # Создаем новый ContentFile с фиксированным именем
            self.phrases.save(name=filename, content=ContentFile(content), save=False)
        else:
            # Если новый файл не был прикреплен, проверяем существование записи
            if not self.pk and BotPhrases.objects.exists():
                # Используем существующий экземпляр
                existing_instance = BotPhrases.objects.first()
                # Копируем файл из существующей записи, если он есть
                if existing_instance.phrases:
                    content = existing_instance.phrases.read()
                    self.phrases.save(name=filename, content=ContentFile(content), save=False)

        # Вызываем родительский метод save
        super(BotPhrases, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Файл фраз бота"
        verbose_name_plural = "Файлы фраз бота"

    def __str__(self):
        return f"Фразы бота | {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

def get_phrases_orm_object():
    """ Достает файл с фразами бота из БД. """
    try:
        bot_phrase = BotPhrases.objects.first()
        if bot_phrase:
            return bot_phrase
        return HttpResponseNotFound("Файл с фразами не найден.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Запись не найдена.")
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=400)