from django.db import models
from multiselectfield import MultiSelectField

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

REGISTERED_TYPES = (
    ('survey', 'Survey Participation'),
    ('registration', 'Course Registration'),
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
    registeredType = models.CharField(max_length=20, choices=REGISTERED_TYPES, blank=True, null=True)
    registeredAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.fullname}"

    class Meta:
        db_table = 'bot_users'
        ordering = ['-registeredAt']


# TODO: refactor
GENDERS = (
    ('male', 'Male'),
    ('female', 'Female'),
)

COURSE_NUMBERS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)

EDUCATION_TYPES = (
    ('daytime', 'Daytime'),
    ('evening', 'Evening'),
    ('externally', 'Externally')
)

EDUCATION_DIRECTIONS = [
    ('software_engineering', 'Software Engineering'),  # Dasturiy injiniring
    ('computer_engineering', 'Computer Engineering'),  # Kompyuter injiniringi
    ('banking', 'Banking'),  # Bank ishi
    ('finance_and_financial_technologies', 'Finance and Financial Technologies'),  # Moliya va moliyaviy texnologiyalar
    ('logistics', 'Logistics'),  # Logistika
    ('economics', 'Economics'),  # Iqtisodiyot
    ('accounting', 'Accounting'),  # Buxgalteriya hisobi
    ('tourism_and_hospitality', 'Tourism and Hospitality'),  # Turizm va mehmondo’stlik
    ('preschool_education', 'Preschool Education'),  # Maktabgacha taʼlim
    ('primary_education', 'Primary Education'),  # Boshlangʻich taʼlim
    ('special_pedagogy', 'Special Pedagogy'),  # Maxsus pedagogika
    ('native_language_and_literature', 'Native Language and Literature'),  # Ona tili va adabiyot
    ('foreign_language_and_literature', 'Foreign Language and Literature'),  # Xorijiy til va adabiyoti
    ('history', 'History'),  # Tarix
    ('mathematics', 'Mathematics'),  # Matematika
    ('psychology', 'Psychology'),  # Psixologiya
    ('architecture', 'Architecture'),  # Arxitektura
    ('social_work', 'Social Work'),  # Ijtimoiy ish
]

ENGLISH_LEVELS = (
    ('none', 'No knowledge'),
    ('little', 'A little knowledge'),
    ('average', 'Average knowledge'),
    ('good', 'Good (Intermediate and above)'),
)

GOALS = (
    ('career', 'Good career'),
    ('knowledge', 'Acquiring knowledge'),
    ('abroad', 'Work or study abroad'),
    ('entertainment', 'Understand movies/music'),
    ('certificate', 'Get certificate for university'),
)

DAYS_PER_WEEK_CHOICES = (
    (1, '1 - 2 days per week'),
    (2, '3 days per week'),
    (3, 'all days per week'),
)

LEARNING_EXPERIENCE_CHOICES = (
    ('offline', 'In an offline learning center'),
    ('online', 'On online platforms'),
    ('self_taught', 'Self-taught'),
    ('no_experience', 'I have not had the opportunity to learn'),
)

OBSTACLE_CHOICES = (
    ('no_time', 'I didn’t have enough time'),
    ('no_qualified_teachers', 'There were no qualified teachers'),
    ('no_motivation', 'Lacked motivation'),
    ('too_expensive', 'It was too expensive'),
    ('center_too_far', 'The learning center was far away'),
    ('no_obstacles', 'No obstacles'),
)

START_LEARNING_IMPORTANCE_CHOICES = (
    ('start_now', 'I am ready to start now'),
    ('study_later', 'I can study later'),
    ('self_study', 'I want to study on my own'),
    ('not_needed', 'I don’t need English for now'),
)

ENGLISH_PROFICIENCY_CHOICES = (
    ('ielts', "I want to obtain an IELTS certificate"),
    ('fluent', "I want to speak English fluently"),
    ('academic', "I want to read scientific publications and books in English"),
    ('career', "It’s enough for my career"),
)

COURSE_TYPES = (
    ('offline', "Offline"),
    ('online', "Online"),
)

CONDITIONS_CHOICES = (
    ('quality_teaching', "If there is quality education and qualified teachers"),
    ('additional_tutor', "If there is an additional tutor for extra activities"),
    ('free_materials', "If Oxford system books and notebooks are provided for free"),
    ('close_location', "If the location is nearby"),
    ('modern_conditions', "If classes are held in modern conditions using the Oxford system"),
    ('friendly_environment', "If I can learn with like-minded peers in a friendly environment"),
    ('regular_events', "If regular events and competitions are organized in English"),
    ('english_only', "If there is an environment where only English is spoken"),
    ('tours', "If excursions to tourist places are organized"),
    ('study_abroad_support', "If there is assistance in applying to study abroad"),
    ('affordable_prices', "If the prices are reasonable"),
)

CONSIDER_ENROLLMENT_CHOICES = (
    ('yes', "I would consider enrolling"),  # "Qatnashib ko'rgan bo'lardim"
    ('no', "No, I'm not interested at the moment"),  # "Yo'q, hozircha qiziq emas"
)

FREE_LESSON_PARTICIPATION_CHOICES = (
    ('yes', "Yes, I will try attending the free open lesson"),  # "Ha, bepul ochiq darsga qatnashib ko'raman"
    ('no', "No, I don't need it at the moment")  # "Yo'q, hozircha kerak emas"
)


class Survey(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='surveys')
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True)
    courseNumber = models.IntegerField(choices=COURSE_NUMBERS, blank=True, null=True)
    educationType = models.CharField(max_length=20, choices=EDUCATION_TYPES, blank=True, null=True)
    educationDirection = models.CharField(max_length=50, choices=EDUCATION_DIRECTIONS, blank=True, null=True)
    englishLevel = models.CharField(max_length=20, choices=ENGLISH_LEVELS, blank=True, null=True)
    englishGoal = models.CharField(max_length=20, choices=GOALS, blank=True, null=True)
    daysPerWeek = models.PositiveIntegerField(choices=DAYS_PER_WEEK_CHOICES, blank=True, null=True)
    learningExperience = models.CharField(max_length=20, choices=LEARNING_EXPERIENCE_CHOICES, blank=True, null=True)
    obstacles = MultiSelectField(choices=OBSTACLE_CHOICES, blank=True, null=True)
    startLearning_importance = models.CharField(
        max_length=20,
        choices=START_LEARNING_IMPORTANCE_CHOICES,
        blank=True,
        null=True
    )
    importanceRanking = models.TextField(
        blank=True,
        null=True,
        help_text="Please rank the importance of the following factors (1-5) in order: "
                  "1. Quality teaching and qualified instructors, "
                  "2. Location, "
                  "3. Modern facilities and a friendly environment, "
                  "4. Activities (Movie day, Speaking club, Competitions), "
                  "5. Affordability. "
                  "For example: 3, 2, 1, 5, 4"
    )
    englishProficiency = models.CharField(
        max_length=20,
        choices=ENGLISH_PROFICIENCY_CHOICES,
        blank=True,
        null=True,
        help_text="Please select your English level. For example: I want to obtain an IELTS certificate"
    )
    courseType = models.CharField(
        max_length=10,
        choices=COURSE_TYPES,
        blank=True,
        null=True,
        help_text="Choose the type of education that suits you."
    )
    conditions = MultiSelectField(choices=CONDITIONS_CHOICES, blank=True, null=True)
    considerEnrollment = models.CharField(
        max_length=3,
        choices=CONSIDER_ENROLLMENT_CHOICES,
        blank=True,
        null=True
    )
    freeLessonParticipation = models.CharField(
        max_length=3,
        choices=FREE_LESSON_PARTICIPATION_CHOICES,
        blank=True,
        null=True,
        help_text="Would you like to attend the free open lesson?"
    )

    objects = models.Manager()

    def __str__(self):
        return self.user.fullname

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"
        ordering = ['-user__registeredAt']
