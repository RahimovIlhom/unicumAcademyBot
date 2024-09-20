from django.db import models

from users.models import LEVELS
from users.models import BotUser


class Question(models.Model):
    level = models.CharField(max_length=20, choices=LEVELS)
    image = models.ImageField(blank=True, null=True, upload_to='questions/images/')
    question = models.TextField(blank=True, null=True)
    a = models.CharField(max_length=1000, verbose_name="Correct answer")
    b = models.CharField(max_length=1000)
    c = models.CharField(max_length=1000)
    d = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level}: question-{self.pk}"

    class Meta:
        db_table = 'questions'


class TestResult(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVELS)
    totalQuestions = models.IntegerField()
    correctAnswers = models.IntegerField()
    scorePercentage = models.DecimalField(max_digits=5, decimal_places=2)
    resultScore = models.DecimalField(max_digits=5, decimal_places=2)
    resultDataJSON = models.JSONField()
    recommendedLevel = models.CharField(max_length=20, choices=LEVELS, blank=True, null=True)
    resultedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.fullname}: {self.resultScore}"

    class Meta:
        db_table = 'test_results'
