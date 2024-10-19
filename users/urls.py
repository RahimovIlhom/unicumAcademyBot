from django.urls import path

from .views.users_views import ExportUsersToExcel, get_levels_for_telegram_user, SurveyCreateView, SurveyRetrieveView, \
    ExportSurveysToExcel
from .views.stats_views import GenderStatsAPIView, AgeStatsAPIView, CourseNumberStatsAPIView

urlpatterns = [
    path('users/export/excel/', ExportUsersToExcel.as_view(), name='export_excel'),
    path('users/levels/bot-user/', get_levels_for_telegram_user, name='get_levels_for_telegram_user'),
    path('users/survey/create/', SurveyCreateView.as_view(), name='survey_create'),
    path('users/survey/<int:userId>/', SurveyRetrieveView.as_view(), name='survey_update'),
    path('users/export/survey/', ExportSurveysToExcel.as_view(), name='export_survey'),

    path('stats/genders/', GenderStatsAPIView.as_view(), name='get_genders_stats'),
    path('stats/ages/', AgeStatsAPIView.as_view(), name='get_ages_stats'),
    path('stats/courses/', CourseNumberStatsAPIView.as_view(), name='get_courses_stats'),
]
