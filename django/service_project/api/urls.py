from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalDataViewSet, BotOrderViewSet, SupportRequestViewSet, UserSettingViewSet

router = DefaultRouter()
router.register(r'personaldata', PersonalDataViewSet)
router.register(r'botorder', BotOrderViewSet)
router.register(r'supportrequest', SupportRequestViewSet)
router.register(r'user-setting', UserSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]