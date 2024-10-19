from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, F

from users.models import Survey, GENDERS
from users.serializers.stats_serializers import GenderStatsSerializers, AgeStatsSerializers, CourseNumberStatsSerializers


class GenderStatsAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Jins statistikasi",
        responses={200: GenderStatsSerializers(many=False)},
    )
    def get(self, request):
        totalCount = Survey.objects.count()
        gender_stats = Survey.objects.values('gender').annotate(count=Count('gender'))
        context = {
            'name': 'gender',
            'totalCount': totalCount,
            'stats': [
                {
                    'name': gender.get('gender'),
                    'count': gender.get('count'),
                    'percentage': round(gender.get('count') / totalCount * 100, 2) if totalCount else 0
                }
                for gender in gender_stats
            ]
        }
        return Response(context, status=200)


class AgeStatsAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Yosh statistikasi",
        responses={200: AgeStatsSerializers(many=False)},
    )
    def get(self, request):
        totalCount = Survey.objects.count()
        answers = Survey.objects.values_list('age', flat=True)
        context = {
            'name': 'age',
            'totalCount': totalCount,
            'answers': list(answers)
        }
        return Response(context, status=200)


class CourseNumberStatsAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Kurs statistikasi",
        responses={200: CourseNumberStatsSerializers(many=False)},
    )
    def get(self, request):
        totalCount = Survey.objects.count()
        course_stats = Survey.objects.values('courseNumber').annotate(count=Count('courseNumber'))
        context = {
            'name': 'courseNumber',
            'totalCount': totalCount,
            'stats': [
                {
                    'name': course.get('courseNumber'),
                    'totalCount': course.get('count'),
                    'percentage': round(course.get('count') / totalCount * 100, 2) if totalCount else 0
                }
                for course in course_stats
            ]
        }
        return Response(context, status=200)
