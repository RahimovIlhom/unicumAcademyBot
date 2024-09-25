from django.db import models
from django.utils import timezone

from users.models import LEVELS
from users.models import BotUser


class Question(models.Model):
    level = models.CharField(max_length=20, choices=LEVELS)
    image = models.ImageField(blank=True, null=True, upload_to='questions/images/')
    question = models.TextField(blank=True, null=True)
    a = models.CharField(max_length=1000, verbose_name="Correct answer")
    b = models.CharField(max_length=1000)
    c = models.CharField(max_length=1000)
    d = models.CharField(max_length=1000, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.level} - qID: {self.pk}"

    def delete(self, using=None, keep_parents=False):
        self.isActive = False
        self.save()

    class Meta:
        db_table = 'questions'


class QuestionResponse(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test_session = models.ForeignKey('TestSession', on_delete=models.CASCADE, related_name='question_responses')  # Add a ForeignKey to TestSession
    answer = models.CharField(max_length=1, null=True, blank=True)  # a, b, c, d
    correct = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user} - {self.question}, answer: {self.answer}"

    class Meta:
        db_table = 'question_responses'
        ordering = ['-id']


class ActiveTestSessionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(completed=False)


class TestSession(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVELS)
    totalQuestions = models.IntegerField(default=20)
    correctAnswers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    completedAt = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveTestSessionManager()

    def __str__(self):
        return f"{self.user} - {self.level}"

    class Meta:
        db_table = 'test_sessions'
        ordering = ['-createdAt']

    def update_correct_answers(self):
        """This method updates the correct answer count based on the responses."""
        correct_responses = self.question_responses.filter(correct=True).count()
        self.correctAnswers = correct_responses
        self.completedAt = timezone.now()
        self.save()
