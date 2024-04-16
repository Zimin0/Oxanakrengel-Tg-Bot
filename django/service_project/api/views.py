from django.shortcuts import render

from rest_framework import viewsets
from order.models import PersonalData, BotOrder
from support.models import SupportRequest
from user_setting.models import Setting
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import PersonalDataSerializer, SupportRequestSerializer, BotOrderSerializer, UserSettingSerializer

class PersonalDataViewSet(viewsets.ModelViewSet):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

class BotOrderViewSet(viewsets.ModelViewSet):
    queryset = BotOrder.objects.all()
    serializer_class = BotOrderSerializer

class SupportRequestViewSet(viewsets.ModelViewSet):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer 

class UserSettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = UserSettingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']