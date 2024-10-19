from rest_framework import serializers


class GenderSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, help_text="Gender name")
    count = serializers.IntegerField(read_only=True)
    percentage = serializers.FloatField(read_only=True)


class GenderStatsSerializers(serializers.Serializer):
    name = serializers.CharField(read_only=True, help_text="Question name")
    totalCount = serializers.IntegerField(read_only=True)
    stats = GenderSerializer(many=True)
