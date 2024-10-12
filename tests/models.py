from django.db import models
from django.utils import timezone

from users.models import LEVELS
from users.models import BotUser


class ActiveQuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isActive=True)


class Question(models.Model):
    level = models.CharField(max_length=20, choices=LEVELS, verbose_name="Daraja")
    image = models.ImageField(blank=True, null=True, upload_to='questions/images/', verbose_name="Rasm")
    question = models.TextField(blank=True, null=True, verbose_name="Savol")
    a = models.CharField(max_length=1000, verbose_name="To'g'ri javob")
    b = models.CharField(max_length=1000, verbose_name="Variant B")
    c = models.CharField(max_length=1000, verbose_name="Variant C")
    d = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Variant D")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    isActive = models.BooleanField(default=True, verbose_name="Faol")

    active_objects = ActiveQuestionManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.level} - qID: {self.pk}"

    def delete(self, using=None, keep_parents=False):
        self.isActive = False
        self.save()

    class Meta:
        db_table = 'questions'
        verbose_name = "Savol "
        verbose_name_plural = "Savollar"


class QuestionResponse(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Savol")
    test_session = models.ForeignKey('TestSession', on_delete=models.CASCADE, related_name='question_responses', verbose_name="Test sessiyasi")
    answer = models.CharField(max_length=1, null=True, blank=True, verbose_name="Javob (a, b, c, d)")
    correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")

    objects = models.Manager()

    def __str__(self):
        return f"{self.user} - {self.question}, javob: {self.answer}"

    class Meta:
        db_table = 'question_responses'
        ordering = ['-id']
        verbose_name = "Savol javobi "
        verbose_name_plural = "Savol javoblari"


class ActiveTestSessionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(completed=False)


class TestSession(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    level = models.CharField(max_length=20, choices=LEVELS, verbose_name="Daraja")
    totalQuestions = models.IntegerField(default=20, verbose_name="Jami savollar")
    correctAnswers = models.IntegerField(default=0, verbose_name="To'g'ri javoblar soni")
    completed = models.BooleanField(default=False, verbose_name="Tamomlanganmi?")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Boshlagan vaqt")
    completedAt = models.DateTimeField(null=True, blank=True, verbose_name="Tamomlangan vaqt")

    objects = models.Manager()
    active_objects = ActiveTestSessionManager()

    def __str__(self):
        return f"{self.user} - {self.level}"

    class Meta:
        db_table = 'test_sessions'
        ordering = ['-createdAt']
        verbose_name = "Test sessiyasi "
        verbose_name_plural = "Test sessiyalari"

    def update_correct_answers(self):
        """This method updates the correct answer count based on the responses."""
        correct_responses = self.question_responses.filter(correct=True).count()
        self.correctAnswers = correct_responses
        self.completedAt = timezone.now()
        self.save()
