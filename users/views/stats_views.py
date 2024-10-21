from collections import Counter

from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Survey
from users.serializers.stats_serializers import FieldStatsSerializer


class BaseSurveyStatsAPIView(APIView):
    field_name = None

    def get(self, request):
        if not self.field_name:
            return Response({"error": "Field name is not specified"}, status=400)

        total_count = Survey.objects.count()

        # Null qiymatlar uchun "None" ni o'z ichiga oluvchi ma'lumotlarni olib kelamiz
        field_data = Survey.objects.values(self.field_name).annotate(
            count=Count(self.field_name)
        )

        # Null qiymatlar sonini to'g'ri hisoblash uchun
        null_count = Survey.objects.filter(**{f"{self.field_name}__isnull": True}).count()

        # Natijalar ro'yxati
        stats = [
            {
                "name": item.get(self.field_name),
                "count": item["count"],
                "percentage": round((item["count"] / total_count) * 100, 2) if total_count else 0
            }
            for item in field_data if item.get(self.field_name) is not None
        ]

        # Agar null qiymatlar mavjud bo'lsa, ularni ham qo'shamiz
        if null_count:
            stats.append({
                "name": None,
                "count": null_count,
                "percentage": round((null_count / total_count) * 100, 2) if total_count else 0
            })

        return Response({
            "question": self.field_name,
            "totalCount": total_count,
            "stats": stats
        })


class GenderStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "gender"

    @swagger_auto_schema(
        operation_summary="Jinsi statistikasi",
        operation_description="Jinsi statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class CourseNumberStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "courseNumber"

    @swagger_auto_schema(
        operation_summary="Talabalarning kursi bo'yicha statistikasi",
        operation_description="Talabalarning kursi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class EducationTypeStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "educationType"

    @swagger_auto_schema(
        operation_summary="Ta'lim turi bo'yicha statistikasi",
        operation_description="Ta'lim turi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class EducationDirectionStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "educationDirection"

    @swagger_auto_schema(
        operation_summary="Ta'lim yo'nalishi bo'yicha statistikasi",
        operation_description="Ta'lim yo'nalishi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class EnglishLevelStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "englishLevel"

    @swagger_auto_schema(
        operation_summary="Ingliz tilini bilish darajasi bo'yicha statistikasi",
        operation_description="Ingliz tilini bilish darajasi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class EnglishGoalStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "englishGoal"

    @swagger_auto_schema(
        operation_summary="Ingliz tilini o'rganish maqsadi bo'yicha statistikasi",
        operation_description="Ingliz tilini o'rganish maqsadi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class DaysPerWeekStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "daysPerWeek"

    @swagger_auto_schema(
        operation_summary="Haftada qancha kunlari bo'yicha statistikasi",
        operation_description="Haftada qancha kunlari bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class LearningExperienceStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "learningExperience"

    @swagger_auto_schema(
        operation_summary="O'qish tajribasi bo'yicha statistikasi",
        operation_description="O'qish tajribasi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class ObstacleStatsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="To'sqinliklar statistikasi",
        operation_description="To'sqinliklar statistikasini qaytaradi.",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'question': openapi.Schema(type=openapi.TYPE_STRING, description='Savol'),
                        'totalCount': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                    description='Umumiy soni'),
                        'stats': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='Tanlangan qiymat'),
                                    'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                            description='Tanlangan qiymat soni'),
                                    'percentage': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE,
                                                                 description='Tanlangan qiymatning foizi'),
                                }
                            ),
                        ),
                    },
                ),
            ),
            400: 'Invalid request',
        }
    )
    def get(self, request):
        # Barcha "obstacles" maydonidagi tanlangan qiymatlarni olish
        obstacle_values = Survey.objects.values_list('obstacles', flat=True).distinct()

        # Har bir tanlangan qiymatni tahlil qilish
        all_choices = []
        for value in obstacle_values:
            if value:
                all_choices.extend(value)

        # Umumiy tanlangan foydalanuvchilar sonini hisoblash
        user_count = Survey.objects.filter(obstacles__isnull=False).distinct().count()

        # Tanlangan qiymatlarning hisobini olish
        count_data = Counter(all_choices)

        stats = [
            {
                "name": key,
                "count": count,
                "percentage": round((count / user_count) * 100, 2) if user_count else 0
            }
            for key, count in count_data.items()
        ]

        return Response({
            "question": "obstacles",
            "totalCount": user_count,
            "stats": stats
        })


class StartLearningImportanceStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "startLearning_importance"

    @swagger_auto_schema(
        operation_summary="Ingliz tilini boshlash ahamiyati statistikasi",
        operation_description="Ingliz tilini boshlash ahamiyati statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class EnglishProficiencyStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "englishProficiency"

    @swagger_auto_schema(
        operation_summary="O'rganishdan maqsad statistikasi",
        operation_description="O'rganishdan maqsad statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class CourseTypeStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "courseType"

    @swagger_auto_schema(
        operation_summary="Ingliz tili kurs turi bo'yicha statistikasi",
        operation_description="Ingliz tili kurs turi bo'yicha statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class ConditionStatsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Sharoitlarni statistikasi",
        operation_description="Sharoitlarni statistikasi qaytaradi.",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'question': openapi.Schema(type=openapi.TYPE_STRING, description='Savol'),
                        'totalCount': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                    description='Umumiy foydalanuvchilar soni'),
                        'stats': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='Tanlangan qiymat'),
                                    'count': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                            description='Tanlangan qiymat soni'),
                                    'percentage': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE,
                                                                 description='Tanlangan qiymat hisoblanishi'),
                                }
                            ),
                        ),
                    },
                ),
            ),
            400: 'Invalid request',
        }
    )
    def get(self, request):
        # Barcha "conditions" maydonidagi tanlangan qiymatlarni olish
        condition_values = Survey.objects.values_list('conditions', flat=True).distinct()

        # Har bir tanlangan qiymatni tahlil qilish
        all_choices = []
        for value in condition_values:
            if value:
                all_choices.extend(value)

        # Umumiy tanlangan foydalanuvchilar sonini hisoblash
        user_count = Survey.objects.filter(conditions__isnull=False).distinct().count()

        # Tanlangan qiymatlarning hisobini olish
        count_data = Counter(all_choices)

        stats = [
            {
                "name": key,
                "count": count,
                "percentage": round((count / user_count) * 100, 2) if user_count else 0
            }
            for key, count in count_data.items()
        ]

        return Response({
            "question": "conditions",
            "totalCount": user_count,
            "stats": stats
        })


class ConsiderEnrollmentStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "considerEnrollment"

    @swagger_auto_schema(
        operation_summary="O'qishni xohlovchilar statistikasi",
        operation_description="O'qishni xohlovchilar statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class FreeLessonParticipationStatsAPIView(BaseSurveyStatsAPIView):
    field_name = "freeLessonParticipation"

    @swagger_auto_schema(
        operation_summary="Bepul ochiq darsga qatnashish statistikasi",
        operation_description="Bepul ochiq darsga qatnashish statistikasini qaytaradi.",
        responses={
            200: FieldStatsSerializer(),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        return super().get(request)


class AgeStatsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Yoshlarni statistikasi",
        operation_description="Yoshlarni statistikasi qaytaradi.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "values": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        age_data = Survey.objects.values_list('age', flat=True).exclude(age__isnull=True).distinct()

        return Response({
            "values": list(age_data)
        })


class ImportanceRankingStatsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Muhimlik tartibi statistikasi",
        operation_description="Muhimlik tartibi statistikasi qaytaradi.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "values": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Xato xabari")
                }
            )
        }
    )
    def get(self, request):
        ranking_data = Survey.objects.values_list('importanceRanking', flat=True).exclude(
            importanceRanking__isnull=True).distinct()

        return Response({
            "values": list(ranking_data)
        })