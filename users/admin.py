from django.contrib import admin

from .models import BotUser, Survey


class BotUserAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'telegramContact', 'phoneNumber', 'selectedLevel', 'confirmedLevel', 'preferred_time_slot', 'registeredType', 'registeredAt', 'updatedAt']
    list_filter = ['selectedLevel', 'confirmedLevel', 'recommendedLevel']
    search_fields = ['telegramId', 'fullname', 'telegramContact', 'phoneNumber']

    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(registeredType='registration')
        return queryset


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'get_fullname',
        'get_telegram_contact',
        'get_phone_number',
        'age',
        'gender',
        'courseNumber',
        'educationType',
        'educationDirection',
        'englishLevel',
        'englishGoal',
        'daysPerWeek',
        'learningExperience',
        'startLearning_importance',
        'importanceRanking',
        'englishProficiency',
        'courseType',
        'considerEnrollment',
        'freeLessonParticipation',
    )

    list_filter = ('age', 'gender', 'courseNumber', 'englishLevel', 'daysPerWeek', 'courseType', 'considerEnrollment',
                   'freeLessonParticipation')

    search_fields = ('user__fullname', 'user__telegramContact', 'user__phoneNumber', 'age', 'gender', 'educationDirection')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def get_fullname(self, obj):
        return obj.user.fullname

    get_fullname.admin_order_field = 'user__fullname'
    get_fullname.short_description = 'FISH'

    def get_telegram_contact(self, obj):
        return obj.user.telegramContact

    get_telegram_contact.admin_order_field = 'user__telegramContact'
    get_telegram_contact.short_description = 'Telegram kontakti'

    def get_phone_number(self, obj):
        return obj.user.phoneNumber

    get_phone_number.admin_order_field = 'user__phoneNumber'
    get_phone_number.short_description = 'Telefon raqami'


admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Survey, SurveyAdmin)
