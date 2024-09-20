import xlsxwriter
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import BotUser


class ExportUsersToExcel(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # BotUser modelidagi barcha foydalanuvchilarni olish
        bot_users = BotUser.objects.all()

        # Javobni HttpResponse orqali Excel formatida qaytarish
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bot_users.xlsx'

        # XlsxWriter bilan yangi workbook yaratish
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet('Bot Users')

        # Sarlavhalarni qo'shish
        headers = [
            "Telegram ID", "Full Name", "Telegram Contact",
            "Phone Number", "Language", "Selected Level",
            "Confirmed Level", "Recommended Level", "Registered At", "Updated At"
        ]

        # Sarlavhalarni qo'shish
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Foydalanuvchilar ma'lumotlarini qo'shish
        for row_num, user in enumerate(bot_users, 1):
            worksheet.write(row_num, 0, user.telegramId)
            worksheet.write(row_num, 1, user.fullname)
            worksheet.write(row_num, 2, user.telegramContact)
            worksheet.write(row_num, 3, user.phoneNumber)
            worksheet.write(row_num, 4, user.language)
            worksheet.write(row_num, 5, user.selectedLevel)
            worksheet.write(row_num, 6, user.confirmedLevel)
            worksheet.write(row_num, 7, user.recommendedLevel)
            worksheet.write(row_num, 8, user.registeredAt.strftime('%Y-%m-%d %H:%M:%S'))
            worksheet.write(row_num, 9, user.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))

        # Workbookni yopish va javobni qaytarish
        workbook.close()
        return response
