from django.urls import path, include
from link_generator.views import generate_link

urlpatterns = [
    path('link/', generate_link, name='link'),
]