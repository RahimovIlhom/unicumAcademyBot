from django.contrib import admin

from .models import BotUser, Survey


class BotUserAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'telegramContact', 'phoneNumber', 'selectedLevel', 'status', 'registeredAt']
    list_filter = ['selectedLevel', 'confirmedLevel', 'recommendedLevel']
    search_fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber']


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'age',
        'gender',
        'courseNumber',
        'educationType',
        'englishLevel',
        'daysPerWeek',
        'considerEnrollment',
        'freeLessonParticipation',
    )

    list_filter = ('gender', 'courseNumber', 'educationType', 'englishLevel', 'daysPerWeek', 'considerEnrollment',
                   'freeLessonParticipation')

    search_fields = ('user__fullname', 'user__telegramId', 'educationDirection')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Survey, SurveyAdmin)
