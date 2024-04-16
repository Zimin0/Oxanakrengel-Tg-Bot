from django.contrib import admin
from user_setting.models import Setting

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
