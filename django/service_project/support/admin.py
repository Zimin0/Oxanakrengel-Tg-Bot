from django.contrib import admin
from .models import SupportRequest

# Регистрация модели SupportRequest в админ-панели
@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'status', 'creation_date')  # Поля, которые будут отображаться в списке объектов
    list_filter = ('status', 'creation_date')  # Фильтры по статусу и дате создания
    search_fields = ('text', 'user__name', 'user__surname', 'user__email')  # Поля, по которым будет работать поиск
    date_hierarchy = 'creation_date'  # Навигация по датам
    # raw_id_fields = ('user',)  # Для большого количества пользователей удобно использовать поиск по ID

