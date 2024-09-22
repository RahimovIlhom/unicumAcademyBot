from rest_framework import serializers

from .models import BotUser


class LevelsResponseSerializer(serializers.Serializer):
    levels = serializers.ListField(child=serializers.CharField())


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber', 'selectedLevel']
