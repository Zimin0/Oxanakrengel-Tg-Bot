from django.contrib import admin

from order.models import BotOrder, PersonalData

@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'id', 'name', 'surname', 'email', 'phone_number')
    search_fields = ('telegram_user_id', 'name', 'surname', 'email', 'phone_number')

@admin.register(BotOrder)
class BotOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'personal_data', 'product_link', 'size', 'shipping_method', 'payment_method', 'price', 'status', 'creation_date', 'update_date')
    list_filter = ('shipping_method', 'payment_method', 'status', 'creation_date')
    search_fields = ('product_link', 'personal_data__name', 'personal_data__surname', 'personal_data__telegram_user_id')
    raw_id_fields = ('personal_data',)
    date_hierarchy = 'creation_date'
    ordering = ('-creation_date',)