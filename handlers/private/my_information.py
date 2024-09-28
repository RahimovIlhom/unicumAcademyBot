import asyncio
import re

from aiogram.enums import ContentType
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from pytz import timezone, utc

from config.data import LEVELS_OBJ
from config.data.time_slots import PREFERRED_TIME_SLOTS_DICT, PREFERRED_TIME_SLOTS
from filters import PrivateFilter
from keyboards.default import information_edit_markup, preferred_time_slots
from loader import dp, db


@dp.message(StateFilter(None), PrivateFilter(), F.text == "📝 Ma'lumotlarim")
async def my_information(message: Message):
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("Ro'yxatdan o'tish uchun /start buyrug'ini bosing")
        return

    # Sana formatini o'zgartirish
    tashkent_tz = timezone('Asia/Tashkent')
    registered_at_utc = user['registeredAt'].replace(tzinfo=utc)
    registered_at = registered_at_utc.astimezone(tashkent_tz).strftime('%H:%M %d/%m/%Y')

    # Darajalarni aniqlash
    selected_level = (
        f"{LEVELS_OBJ[user['selectedLevel']]}\n🔹 <b>Daraja holati</b>: ❌ Tasdiqlanmagan"
        if user['selectedLevel'] else "❌ Test topshirilmagan"
    )
    confirmed_level = (
        f"{LEVELS_OBJ[user['confirmedLevel']]}\n🔹 <b>Daraja holati</b>: ✅ Tasdiqlangan"
        if user['confirmedLevel'] else None
    )
    recommended_level = LEVELS_OBJ[user['recommendedLevel']] if user['recommendedLevel'] else None
    recommended_text = '🎯 <b>Tavsiya etilgan daraja:</b> ' + recommended_level + '\n' if recommended_level and user['recommendedLevel'] != user['confirmedLevel'] else ''

    # Asosiy foydalanuvchi ma'lumotlarini formatlash
    user_info = (
        f"📝 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"👤 <b>Ism-familiya:</b> {user['fullname']}\n"
        f"📱 <b>Telegram kontakt:</b> {user['telegramContact'][3:]}\n"
        f"📞 <b>Qo'shimcha raqam:</b> {user['phoneNumber'][3:]}\n"
        f"⭐ <b>Daraja:</b> {confirmed_level or selected_level}\n"
        f"{recommended_text}"
        f"🕒 <b>Kurs uchun qulay vaqt:</b> {PREFERRED_TIME_SLOTS_DICT.get(user['preferred_time_slot'], 'Xatolik')}\n"
        f"🗓️ <b>Ro'yxatdan o'tilgan sana:</b> {registered_at}"
    )

    # Ma'lumotlarni foydalanuvchiga yuborish
    await message.answer(user_info, parse_mode="HTML", reply_markup=await information_edit_markup())


@dp.message(StateFilter(None), PrivateFilter(), F.text == "✏️ Ismni tahrirlash")
async def set_fullname(message: Message, state: FSMContext):
    await message.answer("Ism-familiyangizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state('set_fullname')


@dp.message(StateFilter('set_fullname'), lambda msg: msg.content_type == ContentType.TEXT)
async def send_fullname(message: Message, state: FSMContext):
    fullname = message.text
    await db.set_fullname(message.from_user.id, fullname)
    await state.clear()

    await message.answer("✅ Ism-familiyangiz muvaffaqiyatli o'zgartirildi.")

    await my_information(message)


@dp.message(StateFilter('set_fullname'), lambda msg: msg.content_type != ContentType.TEXT)
async def send_fullname_error(message: Message):
    await message.delete()
    err_msg = await message.answer("⚠️ <b>Xato ma'lumot!</b>\nIltimos, ism-familiyangizni kiriting:")
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(StateFilter(None), PrivateFilter(), F.text == "📞 Raqamni tahrirlash")
async def set_phone_number(message: Message, state: FSMContext):
    await message.answer("Qo'shimcha telefon raqamingizni kiriting:\nMasalan: +998901234567", reply_markup=ReplyKeyboardRemove())
    await state.set_state('set_phone_number')


@dp.message(StateFilter('set_phone_number'),
            lambda msg: msg.content_type == ContentType.TEXT and re.match(r"^\+?[(]?(998)?[)]?[-\s\.]?([0-9]{2})[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}$", msg.text))
async def send_phone_number(message: Message, state: FSMContext):
    phone_number = message.text
    phone_number = re.sub(r"[\+\-\(\)\s\.]", "", phone_number)

    # Telefon raqamni yangilangan holda 998XXXXXXX formatida saqlash
    if phone_number.startswith("998"):
        pass
    else:
        phone_number=f"998{phone_number}"
    await db.set_phone_number(message.from_user.id, phone_number)
    await state.clear()

    await message.answer("✅ Qo'shimcha telefon raqamingiz muvaffaqiyatli o'zgartirildi.")

    await my_information(message)


@dp.message(StateFilter('set_phone_number'))
async def send_fullname_error(message: Message):
    await message.delete()
    err_msg = await message.answer("⚠️ <b>Xato ma'lumot!</b>\nIltimos, qo'shimcha telefon raqam kiriting:")
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(StateFilter(None), PrivateFilter(), F.text == "🕒 Kurs vaqtini tahrirlash")
async def set_preferred_time_slot(message: Message, state: FSMContext):
    await message.answer("Kursda o'qish uchun qulay vaqtni tanlang:", reply_markup=await preferred_time_slots())
    await state.set_state('set_preferred_time')


@dp.message(StateFilter('set_preferred_time'),
            lambda msg: msg.content_type == ContentType.TEXT and msg.text in PREFERRED_TIME_SLOTS.keys())
async def send_time_slot(message: Message, state: FSMContext):
    time_slot_index = PREFERRED_TIME_SLOTS[message.text]
    await db.set_preferred_time_slot(message.from_user.id, time_slot_index)
    await state.clear()

    await message.answer("✅ Kursda o'qish uchun qulay vaqt muvaffaqiyatli o'zgartirildi.")

    await my_information(message)


@dp.message(StateFilter('set_preferred_time'))
async def send_fullname_error(message: Message):
    await message.delete()
    err_msg = await message.answer("⚠️ <b>Xato ma'lumot!</b>\nIltimos, kursda o'qish uchun qulay vaqtni tanlang:")
    await asyncio.sleep(2)
    await err_msg.delete()
