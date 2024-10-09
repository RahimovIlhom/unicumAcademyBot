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

STATUS_CHOICES = (
    ('draft', 'Draft'),                             # Ro'yxatdan to'liq oxirgacha o'tmagan
    ('registered', 'Registered'),                   # Ro'yxatdan o'tgan (kursga hujjat topshirgan)
    ('test_taken', 'Test Taken'),                   # Darajani tasdiqlash uchun test topshirgan
    ('accepted', 'Accepted'),                       # Qabul qilingan
    ('rejected', 'Rejected'),                       # Qabul qilinmagan
    ('active', 'Active'),                           # O'qiyotgan
    ('suspended', 'Suspended'),                     # To'xtatilgan
    ('completed', 'Successfully Completed'),        # Muvaffaqiyatli tamomlagan
    ('failed', 'Unsuccessfully Completed'),         # Muvaffaqiyatsiz tamomlagan
)


class BotUser(models.Model):
    telegramId = models.BigIntegerField(primary_key=True)
    fullname = models.CharField(max_length=255)
    telegramContact = models.CharField(max_length=20, blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    preferred_time_slot = models.IntegerField(
        choices=PREFERRED_TIME_SLOTS, default=1,
        blank=True, null=True
    )
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    selectedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    confirmedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    recommendedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    registeredAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'bot_users'
        ordering = ['-registeredAt']
