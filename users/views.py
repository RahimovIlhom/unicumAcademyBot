import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import aiohttp
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from config import BOT_TOKEN
from keyboards.default import main_menu, free_lesson_participation
from .models import BotUser, Survey
from .serializers import LevelsResponseSerializer, SurveyCreateSerializer, SurveyRetrieveSerializer
from .utils.data import LEVELS_DICT, LEVELS_LIST
from .utils.surveys_write_excel import export_surveys_to_excel
from .utils.users_write_excel import export_users_to_excel


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

        return export_users_to_excel(response, bot_users)


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


class SurveyCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyCreateSerializer

    @swagger_auto_schema(
        request_body=SurveyCreateSerializer,
        responses={
            201: SurveyCreateSerializer(),
            400: 'Invalid data.',
            404: "No BotUser matches the given query.",
        },
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        bot_user = get_object_or_404(BotUser, telegramId=user_id)

        # Serializerdan foydalanish
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # BotUser statusini yangilash
        bot_user.status = 'registered'
        bot_user.registeredType = 'survey'
        bot_user.save()

        # Xabar yuborish va holatni orqa fonda yangilash
        self.run_in_background(send_message, bot_user.telegramId, serializer.data.get('considerEnrollment'))

        # API response
        return Response(serializer.data)

    def run_in_background(self, func, *args):
        def wrapper():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(*args))
            except Exception as e:
                pass
            finally:
                loop.close()

        # ThreadPoolExecutor yordamida yangi ipda vazifani bajarish
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(wrapper)


async def send_message(user_id, considerEnrollment):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    if considerEnrollment == 'yes':
        reply_markup = await free_lesson_participation()

        payload = {
            'chat_id': user_id,
            'text': "So'rovnomada ishtirok etganingiz uchun rahmat! O'quv markazimizga qiziqish bildiribsiz, bepul ochiq darsimizda ishtirok etib ko'rasizmi?",
            'parse_mode': 'HTML',
            'reply_markup': reply_markup.dict(include=None, exclude_none=True),
        }
    else:
        reply_markup = await main_menu(user_id)

        payload = {
            'chat_id': user_id,
            'text': "So'rovnomada ishtirok etganingiz uchun rahmat!",
            'parse_mode': 'HTML',
            'reply_markup': reply_markup.dict(include=None, exclude_none=True),
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return response.status


class SurveyRetrieveView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SurveyRetrieveSerializer

    @swagger_auto_schema(
        responses={
            200: SurveyRetrieveSerializer(),
            404: "No BotUser matches the given query.",
        },
    )
    def get(self, request, userId, *args, **kwargs):
        bot_user = get_object_or_404(BotUser, telegramId=userId)
        survey = Survey.objects.filter(user=bot_user).order_by('-id').first()
        serializer = self.serializer_class(survey)
        return Response(serializer.data)


class ExportSurveysToExcel(APIView):
    permission_classes = [IsAdminUser]

    # Swagger uchun query parameter va response dokumentatsiyasi
    @swagger_auto_schema(
        responses={
            200: 'Excel fayli muvaffaqiyatli yaratildi va qaytarildi.',
            500: 'Foydalanuvchilarni yozishda xatolik.'
        }
    )
    def get(self, request):
        # Javobni Excel formatida HttpResponse orqali qaytarish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=surveys_all.xlsx'

        return export_surveys_to_excel(response)