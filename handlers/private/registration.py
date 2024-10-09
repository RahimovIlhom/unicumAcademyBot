import asyncio
import re

from aiogram import types
from aiogram.enums import ContentType
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config.data import PREFERRED_TIME_SLOTS
from filters import PrivateFilter
from loader import dp, db
from states import Registration
from keyboards.default import get_contact_markup, main_menu, preferred_time_slots


@dp.message(PrivateFilter(), CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        await start_registration(message, state)
    else:
        if user.get('status') == 'draft':
            await message.answer(
                "Kursda o'qish uchun qulay vaqtni tanlang. Quyidagi tugmalardan birini tanlab, o'z jadvalingizni belgilab oling:",
                reply_markup=await preferred_time_slots()
            )
            await state.set_state(Registration.preferred_time_slot)
            await state.update_data(telegramId=message.from_user.id)
            return
        await message.answer("Bosh menyu", reply_markup=await main_menu(telegramId=message.from_user.id))
        await state.clear()


async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Unicum Academy o’quv markazining rasmiy botiga "
                         "xush kelibsiz. Ingliz tili kursiga ro'yxatdan o'tish uchun "
                         "ism va familiyangizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.name)


# Ismni qabul qilish
@dp.message(Registration.name, lambda msg: msg.content_type == ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(telegramId=message.from_user.id, fullname=message.text)
    await message.answer("Endi quyidagi tugmani bosing va telefon raqamingizni ulashing:",
                         reply_markup=await get_contact_markup())
    await state.set_state(Registration.contact)


# Telegram kontaktini qabul qilish
@dp.message(Registration.contact, lambda msg: msg.content_type==ContentType.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number.replace('+', ''))
    await message.answer("Siz bilan bog’lanishimiz uchun qo'shimcha telefon raqamini kiriting:\n"
                         "Masalan: +998901234567", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.phone)


# Qo'shimcha telefon raqamini qabul qilish
@dp.message(Registration.phone,
            lambda msg: msg.content_type == ContentType.TEXT and re.match(r"^\+?[(]?(998)?[)]?[-\s\.]?([0-9]{2})[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}$", msg.text))
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text

    # Telefon raqamni barcha bo'shliqlar, nuqtalar, qavslar va tirelardan tozalash
    phone = re.sub(r"[\+\-\(\)\s\.]", "", phone)

    if phone in data.get('contact'):
        await message.answer("Qo'shimcha telefon raqami telegram kontaktingiz bilan bir xil bo'lmasligi kerak.\n"
                             "Iltimos, qaytadan kiriting:", reply_markup=ReplyKeyboardRemove())
        return

    # Telefon raqamni yangilangan holda 998XXXXXXX formatida saqlash
    if phone.startswith("998"):
        await state.update_data(phone=phone)
    else:
        await state.update_data(phone=f"998{phone}")

    # databasega saqlash
    data.update(phone=phone)
    await db.add_draft_user(**data)

    await message.answer(
        "Kursda o'qish uchun qulay vaqtni tanlang. Quyidagi tugmalardan birini tanlab, o'z jadvalingizni belgilab oling:",
        reply_markup=await preferred_time_slots()
    )
    await state.set_state(Registration.preferred_time_slot)


@dp.message(Registration.preferred_time_slot, lambda msg: msg.content_type == ContentType.TEXT and msg.text in PREFERRED_TIME_SLOTS.keys())
async def get_preferred_time_slot(message: types.Message, state: FSMContext):
    await state.update_data(preferred_time_slot=PREFERRED_TIME_SLOTS[message.text])
    user_data = await state.get_data()

    # databasega saqlash
    await db.complete_registration(**user_data)
    # state ni tozalash
    await state.clear()

    # Testga taklif qilish
    await message.answer("✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz. Darajangizni aniqlash uchun test topshirishingiz kerak.\n"
                         "🧑‍💻 <b>Test topshirish</b> tugmasini bosing.", reply_markup=await main_menu(telegramId=message.from_user.id))


@dp.message(StateFilter(Registration))
async def error_message(message: types.Message):
    await message.delete()
    er_msg = await message.answer("⚠️ <b>Xato ma'lumot!</b>\nIltimos, ko'rsatmalarga amal qilgan holda kerakli ma'lumotni to'g'ri formatda kiriting.")
    await asyncio.sleep(5)
    await er_msg.delete()
