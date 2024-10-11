from django.urls import path

from .views import ExportUsersToExcel, get_levels_for_telegram_user, SurveyCreateView, SurveyRetrieveView

urlpatterns = [
    path('export/excel/', ExportUsersToExcel.as_view(), name='export_excel'),
    path('levels/bot-user/', get_levels_for_telegram_user, name='get_levels_for_telegram_user'),
    path('survey/create/', SurveyCreateView.as_view(), name='survey_create'),
    path('survey/<int:userId>/', SurveyRetrieveView.as_view(), name='survey_update'),
]