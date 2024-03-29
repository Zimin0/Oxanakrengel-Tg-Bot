from django.shortcuts import render

from rest_framework import viewsets
from order.models import PersonalData, BotOrder
from support.models import SupportRequest
from api.serializers import PersonalDataSerializer, SupportRequestSerializer, BotOrderSerializer

class PersonalDataViewSet(viewsets.ModelViewSet):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

class BotOrderViewSet(viewsets.ModelViewSet):
    queryset = BotOrder.objects.all()
    serializer_class = BotOrderSerializer

class SupportRequestViewSet(viewsets.ModelViewSet):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer