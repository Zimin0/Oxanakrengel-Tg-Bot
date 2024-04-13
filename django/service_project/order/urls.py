from django.urls import path, include
from order.views import catch_yookassa_response


urlpatterns = [
    path('yookassa_info/', catch_yookassa_response, name='catch_yookassa_response'),
]