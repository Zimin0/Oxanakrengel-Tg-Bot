from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from phrase_json.models import BotPhrases

@admin.register(BotPhrases)
class BotPhrasesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'download_file_button']

    def download_file_button(self, obj):
        url = reverse('download_file', args=[obj.id])
        return format_html('<a class="button" href="{}">Скачать файл</a>', url)
    
    download_file_button.short_description = 'Скачать файл'
    download_file_button.allow_tags = True