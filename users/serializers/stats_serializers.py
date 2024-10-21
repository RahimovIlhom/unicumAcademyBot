from rest_framework import serializers


class StatsListSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, help_text="Value name")
    count = serializers.IntegerField(read_only=True)
    percentage = serializers.FloatField(read_only=True)


class FieldStatsSerializer(serializers.Serializer):
    question = serializers.CharField(read_only=True, help_text="Field name")
    totalCount = serializers.IntegerField(read_only=True)
    stats = StatsListSerializer(many=True)
