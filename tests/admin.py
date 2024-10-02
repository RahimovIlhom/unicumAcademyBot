from django.contrib import admin

from .models import Question, QuestionResponse, TestSession


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question', 'a', 'createdAt')
    list_filter = ('level', )
    search_fields = ('question', 'a', 'b', 'c', 'd')
    exclude = ('isActive', )


class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level', 'totalQuestions', 'correctAnswers', 'createdAt')
    list_filter = ('level', )
    search_fields = ('user', 'level', 'correctAnswers')


class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'test_session', 'answer', 'correct')


admin.site.register(Question, QuestionAdmin)

admin.site.register(QuestionResponse, QuestionResponseAdmin)

admin.site.register(TestSession, TestSessionAdmin)
