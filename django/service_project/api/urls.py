from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalDataViewSet, BotOrderViewSet, SupportRequestViewSet

router = DefaultRouter()
router.register(r'personaldata', PersonalDataViewSet)
router.register(r'botorder', BotOrderViewSet)
router.register(r'supportrequest', SupportRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]