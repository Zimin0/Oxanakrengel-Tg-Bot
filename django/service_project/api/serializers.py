from rest_framework import serializers
from order.models import PersonalData, BotOrder
from support.models import SupportRequest

class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = '__all__'

class BotOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotOrder
        fields = '__all__'

class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = '__all__'