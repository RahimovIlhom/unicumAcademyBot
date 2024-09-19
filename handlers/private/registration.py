import asyncio
import re

from aiogram import types
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config import LEVELS
from loader import dp, db
from states import Registration
from keyboards.default import get_contact_markup, levels_markup, main_manu


async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum, Unicum Academy Botiga xush kelibsiz!\n"
                         "Ingliz tili kursiga ro'yxatdan o'tish uchun ism-familiyangizni kiriting:")
    await state.set_state(Registration.name)


# Ismni qabul qilish
@dp.message(Registration.name, lambda msg: msg.content_type == ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Endi quyidagi tugmani bosing va telefon raqamingizni ulashing:",
                         reply_markup=await get_contact_markup())
    await state.set_state(Registration.contact)


# Telegram kontaktini qabul qilish
@dp.message(Registration.contact, lambda msg: msg.content_type==ContentType.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number.replace('+', ''))
    await message.answer("Qo'shimcha telefon raqamingizni kiriting:\n"
                         "Masalan: +998901234567", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.phone)


# Qo'shimcha telefon raqamini qabul qilish
@dp.message(Registration.phone,
            lambda msg: msg.content_type == ContentType.TEXT and re.match(r"^\+?[(]?(998)?[)]?[-\s\.]?([0-9]{2})[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}$", msg.text))
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text

    # Telefon raqamni barcha bo'shliqlar, nuqtalar, qavslar va tirelardan tozalash
    phone = re.sub(r"[\+\-\(\)\s\.]", "", phone)

    # Telefon raqamni yangilangan holda 998XXXXXXX formatida saqlash
    if phone.startswith("998"):
        await state.update_data(phone=phone)
    else:
        await state.update_data(phone=f"998{phone}")

    await message.answer("Ingliz tili darajangizni tanlang:", reply_markup=await levels_markup())
    await state.set_state(Registration.level)


# Ingliz tili darajasini qabul qilish va ma'lumotlarni saqlash
@dp.message(Registration.level, lambda msg: msg.content_type == ContentType.TEXT and msg.text in LEVELS)
async def get_level(message: types.Message, state: FSMContext):
    await state.update_data(telegramId=message.from_user.id, selectedLevel=message.text)
    user_data = await state.get_data()

    # databasega saqlash
    await db.add_user(**user_data)
    # state ni tozalash
    await state.clear()

    # Testga taklif qilish
    await message.answer("✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz. Darajangizni tasdiqlash uchun test topshirishingiz kerak.\n"
                         "'Test boshlash' tugmasini bosing.", reply_markup=await main_manu())


@dp.message(StateFilter(Registration))
async def error_message(message: types.Message):
    await message.delete()
    er_msg = await message.answer("⚠️ <b>Xato ma'lumot!</b>\nIltimos, ko'rsatmalarga amal qilgan holda kerakli ma'lumotni to'g'ri formatda kiriting.")
    await asyncio.sleep(3)
    await er_msg.delete()
