from datetime import timedelta

import xlsxwriter
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import localtime, now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import BotUser, PREFERRED_TIME_SLOTS, LANGUAGES, LEVELS
from .serializers import LevelsResponseSerializer
from .utils.data import LEVELS_DICT, LEVELS_LIST


class ExportUsersToExcel(APIView):
    permission_classes = [IsAdminUser]

    # Swagger uchun query parameter va response dokumentatsiyasi
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                description="Filtr vaqt oralig'i: last_day (so'nggi kun), last_week (so'nggi hafta), last_month (so'nggi oy), yoki all (barcha foydalanuvchilar)",
                type=openapi.TYPE_STRING,
                enum=['last_day', 'last_week', 'last_month', 'all'],
                default='last_day'
            ),
        ],
        responses={
            200: 'Excel fayli muvaffaqiyatli yaratildi va qaytarildi.',
            400: 'Iltimos, oraliqni tanlang.',
            500: 'Foydalanuvchilarni yozishda xatolik.'
        }
    )
    def get(self, request):
        # Foydalanuvchilarni filterlash uchun query parametri
        period = request.GET.get('period', None)  # 'last_day', 'last_week', 'last_month', or 'all'

        # Hozirgi vaqtni olish
        current_time = now()

        # Vaqt oralig'iga qarab filter yaratish
        if period == 'last_day':
            start_time = current_time - timedelta(days=1)
            time_filter = Q(registeredAt__gte=start_time)
            filename_period = start_time.strftime('%d-%m-%Y') + '_to_' + current_time.strftime('%d-%m-%Y')
        elif period == 'last_week':
            start_time = current_time - timedelta(weeks=1)
            time_filter = Q(registeredAt__gte=start_time)
            filename_period = start_time.strftime('%d-%m-%Y') + '_to_' + current_time.strftime('%d-%m-%Y')
        elif period == 'last_month':
            start_time = current_time - timedelta(days=30)
            time_filter = Q(registeredAt__gte=start_time)
            filename_period = start_time.strftime('%d-%m-%Y') + '_to_' + current_time.strftime('%d-%m-%Y')
        elif period == 'all':
            time_filter = Q()  # Hech qanday filter qo'llanmaydi (barcha foydalanuvchilarni olish)
            filename_period = 'all_time'
        else:
            return Response({'detail': 'Iltimos, oraliqni tanlang.'}, status=400)

        # Filterga asoslangan foydalanuvchilarni olish
        bot_users = BotUser.objects.filter(time_filter).order_by('-registeredAt')

        # Javobni Excel formatida HttpResponse orqali qaytarish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=lids_{filename_period}.xlsx'

        # XlsxWriter bilan yangi workbook yaratish
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet('Bot Users')

        # Formatting styles
        bold = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D7E4BC', 'border': 1})
        cell_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
        date_format = workbook.add_format(
            {'num_format': 'yyyy-mm-dd hh:mm:ss', 'border': 1, 'align': 'center', 'valign': 'vcenter'})

        # Ustunlar uchun sarlavhalar
        headers = [
            "Telegram ID", "Full Name", "Telegram Contact", "Phone Number",
            "Preferred Time Slot", "Language", "Selected Level",
            "Confirmed Level", "Recommended Level", "Registered At", "Updated At"
        ]

        # Column widths
        column_widths = [15, 25, 20, 20, 20, 10, 20, 20, 20, 25, 25]

        # Sarlavhalarni birinchi qatorga qo'shish
        for col_num, (header, width) in enumerate(zip(headers, column_widths)):
            worksheet.set_column(col_num, col_num, width)
            worksheet.write(0, col_num, header, bold)

        # Dictionary'larni bir marta yaratish
        preferred_time_slots = dict(PREFERRED_TIME_SLOTS)
        languages = dict(LANGUAGES)
        levels = dict(LEVELS)

        # Foydalanuvchilar ma'lumotlarini qo'shish
        for row_num, user in enumerate(bot_users, 1):
            worksheet.write(row_num, 0, user.telegramId, cell_format)
            worksheet.write(row_num, 1, user.fullname, cell_format)
            worksheet.write(row_num, 2, getattr(user, 'telegramContact', '') or '', cell_format)
            worksheet.write(row_num, 3, getattr(user, 'phoneNumber', '') or '', cell_format)

            # Preferred time slotni string formatida qo'shish
            worksheet.write(row_num, 4, preferred_time_slots.get(user.preferred_time_slot, 'N/A'), cell_format)

            # Language va Level ma'lumotlarini qo'shish
            worksheet.write(row_num, 5, languages.get(user.language, 'N/A'), cell_format)
            worksheet.write(row_num, 6, levels.get(user.selectedLevel, 'N/A'), cell_format)
            worksheet.write(row_num, 7, levels.get(user.confirmedLevel, 'N/A'), cell_format)
            worksheet.write(row_num, 8, levels.get(user.recommendedLevel, 'N/A'), cell_format)

            # DateTimeField maydonlarini mahalliy vaqt zonasida formatlash va timezone'ni olib tashlash
            worksheet.write(row_num, 9, localtime(user.registeredAt).replace(tzinfo=None), date_format)
            worksheet.write(row_num, 10, localtime(user.updatedAt).replace(tzinfo=None), date_format)

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
        400: 'Telegram ID is required.',
        404: 'No BotUser matches the given query.',
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_levels_for_telegram_user(request):
    telegram_id = request.GET.get('telegramId')

    if not telegram_id:
        return Response({'detail': 'Telegram ID is required.'}, status=400)

    user = get_object_or_404(BotUser, telegramId=telegram_id)

    recommended_level = user.recommendedLevel
    selected_level = user.selectedLevel

    if recommended_level and selected_level and LEVELS_DICT[recommended_level] > LEVELS_DICT[selected_level]:
        levels = LEVELS_LIST[LEVELS_DICT[recommended_level]:]
    else:
        if recommended_level == 'beginner':
            levels = LEVELS_LIST[1:2]
        elif recommended_level == 'advanced':
            levels = LEVELS_LIST[5:6]
        else:
            levels = LEVELS_LIST[1:LEVELS_DICT.get(recommended_level, len(LEVELS_LIST)) + 1]

    levels_data = [
        {
            'label': level.title(),
        } for level in levels
    ]

    return Response({'levels': levels_data}, status=200)
