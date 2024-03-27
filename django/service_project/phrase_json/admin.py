from django.contrib import admin

from phrase_json.models import BotPhrases

@admin.register(BotPhrases)
class BotPhrasesAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]