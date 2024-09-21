from django.contrib import admin

from .models import Question, TestResult


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question', 'a', 'createdAt')
    list_filter = ('level', )
    search_fields = ('question', 'a', 'b', 'c', 'd')


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'totalQuestions', 'correctAnswers', 'scorePercentage', 'resultScore', 'recommendedLevel', 'resultedAt')
    list_filter = ('level', )
    search_fields = ('user__fullname', 'user__telegramContact', 'user__phoneNumber')


admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
