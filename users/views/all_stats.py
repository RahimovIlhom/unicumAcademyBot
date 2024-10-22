from collections import Counter
from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Survey, GENDERS, COURSE_NUMBERS, EDUCATION_TYPES, EDUCATION_DIRECTIONS, ENGLISH_LEVELS, GOALS, \
    DAYS_PER_WEEK_CHOICES, LEARNING_EXPERIENCE_CHOICES, START_LEARNING_IMPORTANCE_CHOICES, ENGLISH_PROFICIENCY_CHOICES, \
    COURSE_TYPES, CONSIDER_ENROLLMENT_CHOICES, FREE_LESSON_PARTICIPATION_CHOICES, OBSTACLE_CHOICES, CONDITIONS_CHOICES


class CombinedStatsAPIView(APIView):

    def get_field_stats(self, field_name, stats_dict: dict = {}):
        total_count = Survey.objects.count()

        # Null qiymatlar uchun "None" ni o'z ichiga oluvchi ma'lumotlarni olib kelamiz
        field_data = Survey.objects.values(field_name).annotate(
            count=Count(field_name)
        )

        # Null qiymatlar sonini to'g'ri hisoblash uchun
        null_count = Survey.objects.filter(**{f"{field_name}__isnull": True}).count()

        # Natijalar ro'yxati
        stats = [
            {
                "name": stats_dict.get(item.get(field_name), 'no_data'),
                "count": item["count"],
                "percentage": round((item["count"] / total_count) * 100, 2) if total_count else 0
            }
            for item in field_data if item.get(field_name) is not None
        ]

        # Agar null qiymatlar mavjud bo'lsa, ularni ham qo'shamiz
        if null_count:
            stats.append({
                "name": None,
                "count": null_count,
                "percentage": round((null_count / total_count) * 100, 2) if total_count else 0
            })

        return {
            "question": field_name,
            "totalCount": total_count,
            "stats": stats
        }

    def get_multi_choice_stats(self, field_name, stats_dict: dict = {}):
        # Barcha maydonlardagi tanlangan qiymatlarni olish
        field_values = Survey.objects.values_list(field_name, flat=True).distinct()

        # Har bir tanlangan qiymatni tahlil qilish
        all_choices = []
        for value in field_values:
            if value:
                all_choices.extend(value)

        # Umumiy tanlangan foydalanuvchilar sonini hisoblash
        user_count = Survey.objects.filter(**{f"{field_name}__isnull": False}).distinct().count()

        # Tanlangan qiymatlarning hisobini olish
        count_data = Counter(all_choices)

        stats = [
            {
                "name": stats_dict.get(key, 'no_data'),
                "count": count,
                "percentage": round((count / user_count) * 100, 2) if user_count else 0
            }
            for key, count in count_data.items()
        ]

        return {
            "question": field_name,
            "totalCount": user_count,
            "stats": stats
        }

    def get_simple_value_stats(self, field_name):
        field_data = Survey.objects.values_list(field_name, flat=True).exclude(
            **{f"{field_name}__isnull": True}).distinct()
        return {
            "values": list(field_data)
        }

    @swagger_auto_schema(
        operation_summary="Barcha statistikalarni qaytaruvchi API",
        operation_description="Har xil so'rovlar bo'yicha umumiy statistikani qaytaradi.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "gender": openapi.Schema(type=openapi.TYPE_OBJECT, description="Gender statistikasi"),
                    "courseNumber": openapi.Schema(type=openapi.TYPE_OBJECT, description="Kurs soni statistikasi"),
                    "educationType": openapi.Schema(type=openapi.TYPE_OBJECT, description="Ta'lim turi statistikasi"),
                    "educationDirection": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                         description="Ta'lim yo'nalishi statistikasi"),
                    "englishLevel": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                   description="Ingliz tili darajasi statistikasi"),
                    "englishGoal": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                  description="Ingliz tilini o'rganish maqsadi statistikasi"),
                    "daysPerWeek": openapi.Schema(type=openapi.TYPE_OBJECT, description="Haftada kunlar statistikasi"),
                    "learningExperience": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                         description="O'qish tajribasi statistikasi"),
                    "obstacles": openapi.Schema(type=openapi.TYPE_OBJECT, description="To'sqinliklar statistikasi"),
                    "conditions": openapi.Schema(type=openapi.TYPE_OBJECT, description="Sharoitlar statistikasi"),
                    "startLearning_importance": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                               description="Ingliz tilini boshlash ahamiyati statistikasi"),
                    "englishProficiency": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                         description="Ingliz tili bilish statistikasi"),
                    "courseType": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                 description="Ingliz tili kurs turi statistikasi"),
                    "considerEnrollment": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                         description="O'qishni xohlovchilar statistikasi"),
                    "freeLessonParticipation": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                              description="Bepul ochiq dars statistikasi"),
                    "age": openapi.Schema(type=openapi.TYPE_OBJECT, description="Yoshlar statistikasi"),
                    "importanceRanking": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                        description="Muhimlik tartibi statistikasi"),
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
        response_data = {
            "gender": self.get_field_stats("gender", dict(GENDERS)),
            "courseNumber": self.get_field_stats("courseNumber", dict(COURSE_NUMBERS)),
            "educationType": self.get_field_stats("educationType", dict(EDUCATION_TYPES)),
            "educationDirection": self.get_field_stats("educationDirection", dict(EDUCATION_DIRECTIONS)),
            "englishLevel": self.get_field_stats("englishLevel", dict(ENGLISH_LEVELS)),
            "englishGoal": self.get_field_stats("englishGoal", dict(GOALS)),
            "daysPerWeek": self.get_field_stats("daysPerWeek", dict(DAYS_PER_WEEK_CHOICES)),
            "learningExperience": self.get_field_stats("learningExperience", dict(LEARNING_EXPERIENCE_CHOICES)),
            "obstacles": self.get_multi_choice_stats("obstacles", dict(OBSTACLE_CHOICES)),
            "conditions": self.get_multi_choice_stats("conditions", dict(CONDITIONS_CHOICES)),
            "startLearning_importance": self.get_field_stats("startLearning_importance", dict(START_LEARNING_IMPORTANCE_CHOICES)),
            "englishProficiency": self.get_field_stats("englishProficiency", dict(ENGLISH_PROFICIENCY_CHOICES)),
            "courseType": self.get_field_stats("courseType", dict(COURSE_TYPES)),
            "considerEnrollment": self.get_field_stats("considerEnrollment", dict(CONSIDER_ENROLLMENT_CHOICES)),
            "freeLessonParticipation": self.get_field_stats("freeLessonParticipation", dict(FREE_LESSON_PARTICIPATION_CHOICES)),
            "age": self.get_simple_value_stats("age"),
            "importanceRanking": self.get_simple_value_stats("importanceRanking")
        }

        return Response(response_data)
