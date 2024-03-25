from django.db import models

from order.models import PersonalData 

class SupportRequest(models.Model):
    STATUSES = (
        ('in_progress', 'Ожидает ответа'),
        ('finished', 'Завершена'),
    ) 
    user = models.CharField(verbose_name="Идентификатор пользователя telegram", max_length=100, blank=False)
    text = models.TextField(verbose_name='Запрос', blank=False)
    status = models.CharField(verbose_name="Статус заявки", max_length=60, choices=STATUSES)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        """Возвращает текстовое представление объекта."""
        return f"Заявка от {self.user}, Статус: {self.get_status_display()}"

    class Meta:
        verbose_name = "Запрос в поддержку"
        verbose_name_plural = "Запросы в поддержку"
        ordering = ['-creation_date']