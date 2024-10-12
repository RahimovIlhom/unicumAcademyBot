from users.models import GENDERS, COURSE_NUMBERS, EDUCATION_TYPES, EDUCATION_DIRECTIONS, ENGLISH_LEVELS, GOALS, \
    DAYS_PER_WEEK_CHOICES, LEARNING_EXPERIENCE_CHOICES, OBSTACLE_CHOICES, START_LEARNING_IMPORTANCE_CHOICES, \
    ENGLISH_PROFICIENCY_CHOICES, COURSE_TYPES, CONDITIONS_CHOICES, CONSIDER_ENROLLMENT_CHOICES, \
    FREE_LESSON_PARTICIPATION_CHOICES

genders = dict(GENDERS)
course_numbers = dict(COURSE_NUMBERS)
education_types = dict(EDUCATION_TYPES)
education_directions = dict(EDUCATION_DIRECTIONS)
english_levels = dict(ENGLISH_LEVELS)
goals = dict(GOALS)
days_per_week_choices = dict(DAYS_PER_WEEK_CHOICES)
learning_experience_choices = dict(LEARNING_EXPERIENCE_CHOICES)
obstacles_dict = dict(OBSTACLE_CHOICES)
start_learning_importance_choices = dict(START_LEARNING_IMPORTANCE_CHOICES)
english_proficiency_choices = dict(ENGLISH_PROFICIENCY_CHOICES)
course_types = dict(COURSE_TYPES)
conditions_dict = dict(CONDITIONS_CHOICES)
consider_enrollment = dict(CONSIDER_ENROLLMENT_CHOICES)
free_lesson_participation_choices = dict(FREE_LESSON_PARTICIPATION_CHOICES)
column_widths = [
    15,  # Telegram ID
    25,  # F.I.Sh.
    25,  # Telegram kontakti
    20,  # Telefon raqami
    10,  # Yoshi
    10,  # Jinsi
    15,  # Kurs raqami
    20,  # Ta'lim turi
    25,  # Ta'lim yo'nalishi
    25,  # Ingliz tili darajasi
    30,  # Ingliz tili o'rganish maqsadi
    20,  # Haftada qancha kun
    25,  # O'qish tajribasi
    30,  # To'sqinliklar
    30,  # Ingliz tilini boshlash ahamiyati
    15,  # Muhimlik tartibi
    30,  # O'rganishdan maqsad
    25,  # Kurs turi
    45,  # Sharoitlar
    30,  # O'qishni xohlaysizmi?
    30,  # Bepul ochiq darsga qatnashish
    25   # Ro'yxatdan o'tgan vaqt
]
