from rest_framework import serializers

from .models import BotUser, Survey, OBSTACLE_CHOICES, CONDITIONS_CHOICES


class LevelSerializer(serializers.Serializer):
    label = serializers.CharField()


class LevelsResponseSerializer(serializers.Serializer):
    levels = serializers.ListField(child=LevelSerializer())


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber', 'selectedLevel']


class SurveyCreateSerializer(serializers.ModelSerializer):
    obstacles = serializers.ListField(
        child=serializers.ChoiceField(choices=OBSTACLE_CHOICES)
    )
    conditions = serializers.ListField(
        child=serializers.ChoiceField(choices=CONDITIONS_CHOICES)
    )
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
