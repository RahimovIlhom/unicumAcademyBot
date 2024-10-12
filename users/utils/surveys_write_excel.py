import xlsxwriter
from django.utils.timezone import localtime

from users.models import Survey
from users.utils.survey_choises import genders, course_numbers, education_types, education_directions, english_levels, \
    goals, days_per_week_choices, learning_experience_choices, obstacles_dict, start_learning_importance_choices, \
    english_proficiency_choices, course_types, conditions_dict, consider_enrollment, free_lesson_participation_choices, \
    column_widths


def export_surveys_to_excel(response):
    # Excel faylini yaratish
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet('So\'rovnomalar')

    # Formatting styles
    bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D7E4BC', 'border': 1})
    cell_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    multi_line_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
    date_format = workbook.add_format({'num_format': 'dd-mm-yyyy hh:mm:ss', 'border': 1, 'align': 'center', 'valign': 'vcenter'})

    # Ustunlar uchun sarlavhalar
    headers = [
        "Telegram ID", "F.I.Sh.", "Telegram kontakti", "Telefon raqami",
        "Yoshi", "Jinsi", "Kurs raqami", "Ta'lim turi", "Ta'lim yo'nalishi",
        "Ingliz tili darajasi", "Ingliz tili o'rganish maqsadi", "Haftada qancha kun",
        "O'qish tajribasi", "To'sqinliklar", "Ingliz tilini boshlash ahamiyati",
        "Muhimlik tartibi", "O'rganishdan maqsad", "Kurs turi", "Sharoitlar",
        "O'qishni xohlaysizmi?", "Bepul ochiq darsga qatnashish", "Ro'yxatdan o'tgan vaqt"
    ]

    # Sarlavhalarni birinchi qatorga qo'shish
    for col_num, (header, width) in enumerate(zip(headers, column_widths)):
        worksheet.set_column(col_num, col_num, width)
        worksheet.write(0, col_num, header, bold)

    # Foydalanuvchilar va so'rovnomalar ma'lumotlarini qo'shish
    row_num = 1
    for survey in Survey.objects.select_related('user').order_by('-user__registeredAt'):
        user = survey.user
        worksheet.write(row_num, 0, user.telegramId, cell_format)
        worksheet.write(row_num, 1, user.fullname, cell_format)
        worksheet.write(row_num, 2, user.telegramContact or 'N/A', cell_format)
        worksheet.write(row_num, 3, user.phoneNumber or 'N/A', cell_format)

        # So'rovnoma ma'lumotlarini qo'shish
        worksheet.write(row_num, 4, survey.age or 'N/A', cell_format)
        worksheet.write(row_num, 5, genders.get(survey.gender) or 'N/A', cell_format)
        worksheet.write(row_num, 6, course_numbers.get(survey.courseNumber) or 'N/A', cell_format)
        worksheet.write(row_num, 7, education_types.get(survey.educationType) or 'N/A', cell_format)
        worksheet.write(row_num, 8, education_directions.get(survey.educationDirection) or 'N/A', cell_format)
        worksheet.write(row_num, 9, english_levels.get(survey.englishLevel) or 'N/A', cell_format)
        worksheet.write(row_num, 10, goals.get(survey.englishGoal) or 'N/A', cell_format)
        worksheet.write(row_num, 11, days_per_week_choices.get(survey.daysPerWeek) or 'N/A', cell_format)
        worksheet.write(row_num, 12, learning_experience_choices.get(survey.learningExperience) or 'N/A', cell_format)

        # To'sqinliklar ro'yxatini qo'shish
        obstacles = '\n'.join([obstacles_dict.get(choice, 'N/A') for choice in survey.obstacles]) if survey.obstacles else 'N/A'
        worksheet.write(row_num, 13, obstacles, multi_line_format)

        worksheet.write(row_num, 14, start_learning_importance_choices.get(survey.startLearning_importance) or 'N/A', cell_format)
        worksheet.write(row_num, 15, survey.importanceRanking or 'N/A', cell_format)
        worksheet.write(row_num, 16, english_proficiency_choices.get(survey.englishProficiency) or 'N/A', cell_format)
        worksheet.write(row_num, 17, course_types.get(survey.courseType) or 'N/A', cell_format)

        # Sharoitlar ro'yxatini qo'shish
        conditions = '\n'.join([conditions_dict.get(choice, 'N/A') for choice in survey.conditions]) if survey.conditions else 'N/A'
        worksheet.write(row_num, 18, conditions, multi_line_format)

        worksheet.write(row_num, 19, consider_enrollment.get(survey.considerEnrollment) or 'N/A', cell_format)
        worksheet.write(row_num, 20, free_lesson_participation_choices.get(survey.freeLessonParticipation) or 'N/A', cell_format)

        # Ro'yxatdan o'tgan vaqtni chiroyli formatda yozish
        registered_time = localtime(user.registeredAt).strftime("%Y-%m-%d %H:%M:%S") if user.registeredAt else 'N/A'
        worksheet.write(row_num, 21, registered_time, date_format)

        row_num += 1

    # Excel faylini saqlash
    workbook.close()
    return response
