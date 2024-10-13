from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import Any

from filters import PrivateFilter
from keyboards.default import main_menu
from loader import dp, db
from states import Registration


@dp.message(StateFilter(Any, Registration), PrivateFilter(), F.text == "✅ Ha, bepul ochiq darsga qatnashib ko'raman")
async def set_free_lesson_participant(message: Message, state: FSMContext):
    await db.survey_update_freeLessonParticipation(message.from_user.id, 'yes')
    await message.answer("Zo'r! Operatorlarimiz yaqin vaqt ichida siz bilan bog'lanib, ochiq dars kuni va vaqti haqida ma'lumot berishadi. Kuningiz xayrli o'tsin! ❤️",
                         reply_markup=await main_menu(telegramId=message.from_user.id))
    await state.clear()
    await message.delete()


@dp.message(StateFilter(Any, Registration), PrivateFilter(), F.text == "❌ Yo'q, hozircha kerak emas")
async def set_free_lesson_participant_no(message: Message, state: FSMContext):
    await db.survey_update_freeLessonParticipation(message.from_user.id, 'no')
    await message.answer("Shunday bo'lsada, Unicum Academy ijtimoiy tarmoqlaridagi sahifalarga a'zo bo'lib, yangiliklardan xabardor bo'lib turishingiz mumkin: https://t.me/unicum_academy, https://www.instagram.com/unicum_academy",
                         reply_markup=await main_menu(telegramId=message.from_user.id))
    await state.clear()
    await message.delete()
