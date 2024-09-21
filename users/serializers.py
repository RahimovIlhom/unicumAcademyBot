from rest_framework import serializers


class LevelsResponseSerializer(serializers.Serializer):
    levels = serializers.ListField(child=serializers.CharField())
