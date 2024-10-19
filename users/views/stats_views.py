from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Survey, GENDERS
from users.serializers.stats_serializers import GenderSerializer, GenderStatsSerializers


class GenderStatsAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Jins statistikasi",
        operation_description="Jins statistikasi",
        responses={200: GenderStatsSerializers(many=False)},
    )
    def get(self, request):
        totalCount = Survey.objects.count()
        context = {
            'name': 'gender',
            'totalCount': totalCount,
            'stats': [self.get_gender_stats(gender, totalCount) for gender, _ in GENDERS]
        }
        return Response(context, status=200)

    @staticmethod
    def get_gender_stats(gender: str, totalCount: int) -> dict:
        count = Survey.objects.filter(gender=gender).count()
        return {
            'name': gender,
            'count': count,
            'percentage': round(count / totalCount * 100, 2)
        }
