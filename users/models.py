from django.db import models

LANGUAGES = (
    ('uz', 'Uzbek'),
)

LEVELS = (
    ('beginner', 'Beginner'),
    ('elementary', 'Elementary'),
    ('pre-intermediate', 'Pre-Intermediate'),
    ('intermediate', 'Intermediate'),
    ('upper-intermediate', 'Upper-Intermediate'),
    ('advanced', 'Advanced'),
    ('proficient', 'Proficient'),
)


class BotUser(models.Model):
    telegramId = models.BigIntegerField(primary_key=True)
    fullname = models.CharField(max_length=255)
    telegramContact = models.CharField(max_length=20, blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    selectedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    confirmedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    recommendedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    registeredAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'bot_users'
        ordering = ['-registeredAt']
