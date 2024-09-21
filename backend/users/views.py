import xlsxwriter
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import BotUser
from .serializers import LevelsResponseSerializer
from .utils.data import LEVELS_DICT, LEVELS_LIST


class ExportUsersToExcel(APIView):
    permission_classes = [IsAdminUser]

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


@swagger_auto_schema(
    method='get',  # 'method' orqali aniq metodni ko'rsatamiz
    manual_parameters=[
        openapi.Parameter('telegramId', openapi.IN_QUERY, description="Telegram ID of the user", type=openapi.TYPE_STRING),
    ],
    responses={
        200: LevelsResponseSerializer(),
        400: 'Telegram ID not found',
        404: 'User not found',
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_levels_for_telegram_user(request):
    telegram_id = request.GET.get('telegramId')

    if not telegram_id:
        return Response({'message': 'Telegram ID not found'}, status=400)

    user = BotUser.objects.filter(telegramId=telegram_id).first()

    if not user:
        return Response({'message': 'User not found'}, status=404)

    recommended_level = user.recommendedLevel
    selected_level = user.selectedLevel

    if recommended_level and selected_level and LEVELS_DICT[recommended_level] >= LEVELS_DICT[selected_level]:
        levels = LEVELS_LIST[LEVELS_DICT[recommended_level]:]
    else:
        levels = LEVELS_LIST[:LEVELS_DICT.get(recommended_level, len(LEVELS_LIST)) + 1]

    return Response({'levels': levels}, status=200)


