import xlsxwriter
from django.utils.timezone import localtime

from users.utils.users_choises import headers_users, preferred_time_slots, languages, levels, status_choices, \
    registered_types


def export_users_to_excel(response, bot_users):
    # XlsxWriter bilan yangi workbook yaratish
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet('Bot Users')

    # Formatting styles
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D7E4BC', 'border': 1})
    cell_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    date_format = workbook.add_format(
        {'num_format': 'dd-mm-yyyy hh:mm:ss', 'border': 1, 'align': 'center', 'valign': 'vcenter'})

    # Ustunlar uchun sarlavhalar
    headers = headers_users

    # Column widths
    column_widths = [15, 25, 20, 20, 20, 10, 20, 20, 20, 20, 20, 25, 25]

    # Sarlavhalarni birinchi qatorga qo'shish
    for col_num, (header, width) in enumerate(zip(headers, column_widths)):
        worksheet.set_column(col_num, col_num, width)
        worksheet.write(0, col_num, header, bold)

    # Foydalanuvchilar ma'lumotlarini qo'shish
    for row_num, user in enumerate(bot_users, 1):
        worksheet.write(row_num, 0, user.telegramId, cell_format)
        worksheet.write(row_num, 1, user.fullname, cell_format)
        worksheet.write(row_num, 2, getattr(user, 'telegramContact', '') or '', cell_format)
        worksheet.write(row_num, 3, getattr(user, 'phoneNumber', '') or '', cell_format)

        # Preferred time slotni o'zbekcha formatida qo'shish
        worksheet.write(row_num, 4, preferred_time_slots.get(user.preferred_time_slot, 'N/A'), cell_format)

        # Language va Level ma'lumotlarini qo'shish
        worksheet.write(row_num, 5, languages.get(user.language, 'N/A'), cell_format)
        worksheet.write(row_num, 6, levels.get(user.selectedLevel, 'N/A'), cell_format)
        worksheet.write(row_num, 7, levels.get(user.confirmedLevel, 'N/A'), cell_format)
        worksheet.write(row_num, 8, levels.get(user.recommendedLevel, 'N/A'), cell_format)

        # Status va Registered Typeni o'zbekcha formatida qo'shish
        worksheet.write(row_num, 9, status_choices.get(user.status, 'N/A'), cell_format)
        worksheet.write(row_num, 10, registered_types.get(user.registeredType, 'N/A'), cell_format)

        # DateTimeField maydonlarini mahalliy vaqt zonasida formatlash va timezone'ni olib tashlash
        worksheet.write(row_num, 11, localtime(user.registeredAt).replace(tzinfo=None), date_format)
        worksheet.write(row_num, 12, localtime(user.updatedAt).replace(tzinfo=None), date_format)

    # Workbookni yopish va javobni qaytarish
    workbook.close()
    return response
