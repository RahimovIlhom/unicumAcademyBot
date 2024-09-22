from django.contrib import admin

from .models import Question, QuestionResponse, TestSession


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question', 'a', 'createdAt')
    list_filter = ('level', )
    search_fields = ('question', 'a', 'b', 'c', 'd')


class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level', 'correctAnswers', 'createdAt')
    list_filter = ('level', )
    search_fields = ('user', 'level', 'correctAnswers')


admin.site.register(Question, QuestionAdmin)

admin.site.register(QuestionResponse)

admin.site.register(TestSession)
