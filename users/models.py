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
    (1, '9:00 dan 12:00 gacha'),
    (2, '12:00 dan 15:00 gacha'),
    (3, '15:00 dan 18:00 gacha'),
    (4, '18:00 dan 21:00 gacha'),
)

STATUS_CHOICES = (
    ('draft', 'Qoralama'),                            # Ro'yxatdan to'liq oxirgacha o'tmagan
    ('registered', 'Ro\'yxatdan o\'tgan'),           # Ro'yxatdan o'tgan (kursga hujjat topshirgan)
    ('test_taken', 'Test topshirilgan'),             # Darajani tasdiqlash uchun test topshirgan
    ('accepted', 'Qabul qilingan'),                  # Qabul qilingan
    ('rejected', 'Qabul qilinmagan'),                # Qabul qilinmagan
    ('active', 'Faol'),                              # O'qiyotgan
    ('suspended', 'To\'xtatilgan'),                  # To'xtatilgan
    ('completed', 'Muvaffaqiyatli tamomlangan'),    # Muvaffaqiyatli tamomlagan
    ('failed', 'Muvaffaqiyatsiz tamomlangan'),      # Muvaffaqiyatsiz tamomlagan
)

REGISTERED_TYPES = (
    ('survey', 'So\'rovnomadan o\'tish'),
    ('registration', 'Kursga ro\'yxatdan o\'tish'),
)


class BotUser(models.Model):
    telegramId = models.BigIntegerField(primary_key=True, verbose_name="Telegram ID")
    fullname = models.CharField(max_length=255, verbose_name="FISh")
    telegramContact = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telegram kontakti")
    phoneNumber = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    preferred_time_slot = models.IntegerField(
        choices=PREFERRED_TIME_SLOTS, default=1,
        blank=True, null=True, verbose_name="Afzal vaqt"
    )
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz', verbose_name="Til")
    selectedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True, verbose_name="Tanlangan daraja")
    confirmedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True, verbose_name="Tasdiqlangan daraja")
    recommendedLevel = models.CharField(max_length=20, choices=LEVELS, default=None, blank=True, null=True, verbose_name="Tavsiya etilgan daraja")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Holat")
    registeredType = models.CharField(max_length=20, choices=REGISTERED_TYPES, default='registration', verbose_name="Ro'yxatdan o'tish turi")
    registeredAt = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqt")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    objects = models.Manager()

    def __str__(self):
        return f"{self.fullname}"

    class Meta:
        db_table = 'bot_users'
        ordering = ['-registeredAt']
        verbose_name = 'Foydalanuvchi '
        verbose_name_plural = 'Bot foydalanuvchilari'



# TODO: refactor
GENDERS = (
    ('male', 'Erkak'),
    ('female', 'Ayol'),
)

COURSE_NUMBERS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)

EDUCATION_TYPES = (
    ('daytime', 'Kunduzgi'),
    ('evening', 'Kechki'),
    ('externally', 'Sirtqi')
)

EDUCATION_DIRECTIONS = [
    ('software_engineering', 'Dasturiy injiniring'),  # Software Engineering
    ('computer_engineering', 'Kompyuter injiniringi'),  # Computer Engineering
    ('banking', 'Bank ishi'),  # Banking
    ('finance_and_financial_technologies', 'Moliya va moliyaviy texnologiyalar'),  # Finance and Financial Technologies
    ('logistics', 'Logistika'),  # Logistics
    ('economics', 'Iqtisodiyot'),  # Economics
    ('accounting', 'Buxgalteriya hisobi'),  # Accounting
    ('tourism_and_hospitality', 'Turizm va mehmondo’stlik'),  # Tourism and Hospitality
    ('preschool_education', 'Maktabgacha taʼlim'),  # Preschool Education
    ('primary_education', 'Boshlangʻich taʼlim'),  # Primary Education
    ('special_pedagogy', 'Maxsus pedagogika'),  # Special Pedagogy
    ('native_language_and_literature', 'Ona tili va adabiyot'),  # Native Language and Literature
    ('foreign_language_and_literature', 'Xorijiy til va adabiyoti'),  # Foreign Language and Literature
    ('history', 'Tarix'),  # History
    ('mathematics', 'Matematika'),  # Mathematics
    ('psychology', 'Psixologiya'),  # Psychology
    ('architecture', 'Arxitektura'),  # Architecture
    ('social_work', 'Ijtimoiy ish'),  # Social Work
]

ENGLISH_LEVELS = (
    ('none', 'Umuman bilmayman'),
    ('little', 'Ozgina bilaman'),
    ('average', 'O\'rtacha bilaman'),
    ('good', 'Bilimim yaxshi (intermediate va yuqori)'),
)

GOALS = (
    ('career', 'Kelajakda yaxshi karyera qilish'),
    ('knowledge', 'Ingliz tilida ma\'lumot topib, bilim olish'),
    ('abroad', 'Chet elda ishlash yoki ta\'lim olish'),
    ('entertainment', 'Kino va musiqalarni tushunib ko\'rish, inglizlar bilan gaplashish'),
    ('certificate', 'Magistraturaga kirish uchun sertifikat olish'),
)

DAYS_PER_WEEK_CHOICES = (
    (1, 'Haftada 1 - 2 kun'),
    (2, 'Haftada 3 kun'),
    (3, 'Haftaning barcha kunlari'),
)

LEARNING_EXPERIENCE_CHOICES = (
    ('offline', 'O\'quv markazida (Oflayn)'),
    ('online', 'Onlayn platformalarda'),
    ('self_taught', 'Mustaqil o\'rganganman'),
    ('no_experience', 'O\'rganishga imkoniyatim bo\'lmagan'),
)

OBSTACLE_CHOICES = (
    ('no_time', 'Yetarli vaqt ajrata olmaganman'),
    ('no_qualified_teachers', 'Malakali o‘qituvchilar bo‘lmagan'),
    ('no_motivation', 'Motivatsiya yetishmagan'),
    ('too_expensive', 'Qimmat bo\'lgan'),
    ('center_too_far', 'O‘quv markazi uzoq bo‘lgan'),
    ('no_obstacles', 'Hech qanday to\'sqinlik bo\'lmagan'),
)

START_LEARNING_IMPORTANCE_CHOICES = (
    ('start_now', 'Hoziroq boshlashga tayyorman'),
    ('study_later', 'Keyinchalik o\'qishim mumkin'),
    ('self_study', 'Mustaqil o\'rganmoqchiman'),
    ('not_needed', 'Menga hozircha ingliz tili kerak emas'),
)

ENGLISH_PROFICIENCY_CHOICES = (
    ('ielts', "IELTS sertifikatini olmoqchiman"),
    ('fluent', "Ingliz tilida ravon gaplashmoqchiman"),
    ('academic', "Ingliz tilida ilmiy nashrlar va kitoblarni o'qimoqchiman"),
    ('career', "Karyera qilishim uchun yetarli bo'lsa bo'ldi"),
)

COURSE_TYPES = (
    ('offline', "O'quv markazida (oflayn)"),
    ('online', "Onlayn"),
)

CONDITIONS_CHOICES = (
    ('quality_teaching', "Sifatli ta'lim va malakali ustozlar bo'lsa"),
    ('additional_tutor', "Qo'shimcha shug'ullanadigan ikkinchi ustoz bo'lsa"),
    ('free_materials', "Oxford tizimidagi kitob va daftarlar bepul berilsa"),
    ('close_location', "Lokatsiya yaqin bo'lsa"),
    ('modern_conditions', "Zamonaviy sharoitlarda Oksford tizimida dars o'tilsa"),
    ('friendly_environment', "Do'stona muhitda hamfikr talabalar bilan o'rganilsa"),
    ('regular_events', "Ingliz tilida muntazam tadbirlar va musobaqalar uyushtirilsa"),
    ('english_only', "Faqat ingliz tilida gaplashiladigan muhit bo'lsa"),
    ('tours', "Turistik joylarga ekskursiyalar tashkil qilinsa"),
    ('study_abroad_support', "Chet elda o'qishga hujjat topshirishga yordam berilsa"),
    ('affordable_prices', "Narxlari to'g'ri kelsa"),
)

CONSIDER_ENROLLMENT_CHOICES = (
    ('yes', "Men qatnashib ko'rgan bo'lardim"),
    ('no', "Yo'q, hozircha qiziq emas"),
)

FREE_LESSON_PARTICIPATION_CHOICES = (
    ('yes', "Ha, bepul ochiq darsga qatnashib ko'raman"),
    ('no', "Yo'q, hozircha kerak emas")
)


class Survey(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='surveys', verbose_name="Foydalanuvchi")
    age = models.IntegerField(blank=True, null=True, verbose_name="Yoshi")
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True, verbose_name="Jinsi")
    courseNumber = models.IntegerField(choices=COURSE_NUMBERS, blank=True, null=True, verbose_name="Kurs raqami")
    educationType = models.CharField(max_length=20, choices=EDUCATION_TYPES, blank=True, null=True, verbose_name="Ta'lim turi")
    educationDirection = models.CharField(max_length=50, choices=EDUCATION_DIRECTIONS, blank=True, null=True, verbose_name="Ta'lim yo'nalishi")
    englishLevel = models.CharField(max_length=20, choices=ENGLISH_LEVELS, blank=True, null=True, verbose_name="Ingliz tili darajasi")
    englishGoal = models.CharField(max_length=20, choices=GOALS, blank=True, null=True, verbose_name="Ingliz tili o'rganish maqsadi")
    daysPerWeek = models.PositiveIntegerField(choices=DAYS_PER_WEEK_CHOICES, blank=True, null=True, verbose_name="Haftada qancha kun")
    learningExperience = models.CharField(max_length=20, choices=LEARNING_EXPERIENCE_CHOICES, blank=True, null=True, verbose_name="O'qish tajribasi")
    obstacles = MultiSelectField(choices=OBSTACLE_CHOICES, blank=True, null=True, verbose_name="To'sqinliklar")
    startLearning_importance = models.CharField(
        max_length=20,
        choices=START_LEARNING_IMPORTANCE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Ingliz tilini boshlash ahamiyati",
    )
    importanceRanking = models.TextField(
        blank=True,
        null=True,
        verbose_name="Muhimlik tartibi",
        help_text="Quyidagi omillarning ahamiyatini 1-5 tartibda baholang: "
                  "1. Sifatli ta'lim va malakali o'qituvchilar, "
                  "2. Joylashuv, "
                  "3. Zamonaviy sharoitlar va do'stona muhit, "
                  "4. Tadbirlar (Kinokun, Speaking klubi, Tanlovlar), "
                  "5. Arzon narxlar. "
                  "Masalan: 3, 2, 1, 5, 4"
    )
    englishProficiency = models.CharField(
        max_length=20,
        choices=ENGLISH_PROFICIENCY_CHOICES,
        blank=True,
        null=True,
        verbose_name="O'rganishdan maqsad",
        help_text="Ingliz tilini qay darajada bilish siz uchun yetarli?"
    )
    courseType = models.CharField(
        max_length=10,
        choices=COURSE_TYPES,
        blank=True,
        null=True,
        verbose_name="Kurs turi",
        help_text="O'zingizga mos keladigan ta'lim turini tanlang."
    )
    conditions = MultiSelectField(choices=CONDITIONS_CHOICES, blank=True, null=True, verbose_name="Sharoitlar")
    considerEnrollment = models.CharField(
        max_length=3,
        choices=CONSIDER_ENROLLMENT_CHOICES,
        blank=True,
        null=True,
        verbose_name="O'qishni xohlaysizmi?",
    )
    freeLessonParticipation = models.CharField(
        max_length=3,
        choices=FREE_LESSON_PARTICIPATION_CHOICES,
        blank=True,
        null=True,
        verbose_name="Bepul ochiq darsga qatnashish",
        help_text="Bepul ochiq darsda qatnashishni xohlaysizmi?"
    )

    objects = models.Manager()

    def __str__(self):
        return self.user.fullname

    class Meta:
        db_table = 'surveys'
        verbose_name = "So'rovnoma "
        verbose_name_plural = "So'rovnomalar"
        ordering = ['-user__registeredAt']
