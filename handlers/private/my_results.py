from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from pytz import timezone, utc

from config.data import LEVELS_OBJ
from filters import PrivateFilter
from keyboards.inlines import my_results_markup
from keyboards.inlines.my_results import MyResultCallbackData, one_my_result_markup
from loader import dp, db


@dp.message(StateFilter(None), PrivateFilter(), F.text == '📊 Mening natijam')
async def my_results(message: Message):
    await message.answer("⚠️ Hozirda ushbu funksiya mavjud emas!")
    return
    results = await db.get_my_results(message.from_user.id)
    if not results:
        await message.answer("Sizning hozirda natijangiz mavjud emas. Chunki siz test topshirmagansiz! "
                             "\nIltimos, darajangizni aniqlash uchun \"🧑‍💻 Test topshirish\" tugmasini bosing.")
    else:
        await message.answer("Qaysi test natijangizni ko'rmoqchisiz?\nTanlang:", reply_markup=await my_results_markup(results))


@dp.callback_query(MyResultCallbackData.filter())
async def get_my_result(call: CallbackQuery, callback_data: MyResultCallbackData):
    test_session_id = callback_data.test_session_id
    level = callback_data.level
    if level == -1:
        await call.message.delete()
    elif level == 0:
        await show_results(call)
    elif level == 1:
        await show_my_result(call, test_session_id)


async def show_results(call):
    results = await db.get_my_results(call.from_user.id)
    await call.message.edit_text("Qaysi test natijangizni ko'rmoqchisiz?\nTanlang:", reply_markup=await my_results_markup(results))


async def show_my_result(call, test_session_id):
    result = await db.get_result_by_session_id(test_session_id)

    if not result:
        await call.message.answer("Natija topilmadi.")
        return

    # Sanalarni formatlash
    tashkent_tz = timezone('Asia/Tashkent')
    created_at = result['createdAt'].replace(tzinfo=utc).astimezone(tashkent_tz).strftime('%H:%M %d/%m/%Y') if isinstance(result['createdAt'], datetime) else 'Nomaʼlum'
    completed_at = result['completedAt'].replace(tzinfo=utc).astimezone(tashkent_tz).strftime('%H:%M %d/%m/%Y') if isinstance(result['completedAt'], datetime) else 'Nomaʼlum'

    # Chiroyli tarzda natijalarni formatlash
    result_text = (
        f"<b>{LEVELS_OBJ[result['level']]} darajadagi testingiz natijasi:</b>\n\n"
        f"👤 <b>Foydalanuvchi ID:</b> {result['user_id']}\n"
        f"❓ <b>Umumiy savollar soni:</b> {result['totalQuestions']}\n"
        f"✅ <b>To'g'ri javoblar soni:</b> {result['correctAnswers']}\n"
        f"🗓️ <b>Test boshlangan vaqt:</b> {created_at}\n"
        f"⏱️ <b>Test tugatilgan vaqt:</b> {completed_at if result['completed'] else 'Test hali yakunlanmagan'}\n"
    )

    # Natijani foydalanuvchiga yuborish
    await call.message.edit_text(result_text, parse_mode="HTML", reply_markup=await one_my_result_markup())
