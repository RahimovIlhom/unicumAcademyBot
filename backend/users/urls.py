from django.urls import path

from .views import ExportUsersToExcel

urlpatterns = [
    path('export/excel/', ExportUsersToExcel.as_view(), name='export_excel'),
]