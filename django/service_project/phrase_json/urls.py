from django.urls import path
from .views import get_bot_phrases

urlpatterns = [
    path('bot-phrases/', get_bot_phrases, name='bot-phrases'),
]
