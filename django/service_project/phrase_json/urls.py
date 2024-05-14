from django.urls import path
from .views import get_bot_phrases, download_file_view

urlpatterns = [
    path('bot-phrases/', get_bot_phrases, name='bot-phrases'),
    path('admin/download_file/<int:obj_id>/', download_file_view, name='download_file'),
]
