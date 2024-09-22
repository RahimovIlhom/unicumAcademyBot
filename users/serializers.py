from rest_framework import serializers

from .models import BotUser


class LevelSerializer(serializers.Serializer):
    label = serializers.CharField()


class LevelsResponseSerializer(serializers.Serializer):
    levels = serializers.ListField(child=LevelSerializer())


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber', 'selectedLevel']
