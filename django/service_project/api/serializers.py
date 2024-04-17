from rest_framework import serializers
from order.models import PersonalData, BotOrder
from support.models import SupportRequest
from user_setting.models import Setting

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

class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'