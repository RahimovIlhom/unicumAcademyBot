from django.urls import path

from .views import ExportUsersToExcel, get_levels_for_telegram_user

urlpatterns = [
    path('export/excel/', ExportUsersToExcel.as_view(), name='export_excel'),
    path('levels/bot-user/', get_levels_for_telegram_user, name='get_levels_for_telegram_user'),
]