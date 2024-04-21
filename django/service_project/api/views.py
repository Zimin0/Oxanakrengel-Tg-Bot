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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'telegram_user_id', 'phone_number', 'email']

class BotOrderViewSet(viewsets.ModelViewSet):
    queryset = BotOrder.objects.all()
    serializer_class = BotOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'id', 'personal_data', 'payment_id']


class SupportRequestViewSet(viewsets.ModelViewSet):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'id', 'user']


class UserSettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = UserSettingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']