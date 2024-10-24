from rest_framework import serializers

from tests.models import TestSession
from users.serializers.users_serializers import BotUserSerializer


class QuestionOptionSerializer(serializers.Serializer):
    key = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)


class QuestionSerializer(serializers.Serializer):
    questionId = serializers.IntegerField(read_only=True)
    question = serializers.CharField(read_only=True)
    image = serializers.CharField(allow_null=True)
    options = QuestionOptionSerializer(many=True)


class TestSessionResponseSerializer(serializers.Serializer):
    testSessionId = serializers.IntegerField()
    questions = QuestionSerializer(many=True)
    totalQuestions = serializers.IntegerField()


class TestSessionSerializer(serializers.ModelSerializer):
    user = BotUserSerializer()
    class Meta:
        model = TestSession
        fields = '__all__'


class TestSessionResultSerializer(serializers.Serializer):
    testSession = TestSessionSerializer()
    missingQuestions = serializers.ListField(child=serializers.IntegerField())
