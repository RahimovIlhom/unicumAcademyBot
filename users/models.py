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

PREFERRED_TIME_SLOTS = (
    (1, '9:00 to 12:00'),
    (2, '12:00 to 15:00'),
    (3, '15:00 to 18:00'),
    (4, '18:00 to 21:00'),
)


class BotUser(models.Model):
    telegramId = models.BigIntegerField(primary_key=True)
    fullname = models.CharField(max_length=255)
    telegramContact = models.CharField(max_length=20, blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    preferred_time_slot = models.IntegerField(
        choices=PREFERRED_TIME_SLOTS, default=1
    )
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
