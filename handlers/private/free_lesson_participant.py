from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import PrivateFilter
from keyboards.default import main_menu
from loader import dp, db
from states import Registration


@dp.message(StateFilter(Registration), PrivateFilter(), F.text == "✅ Ha, bepul ochiq darsga qatnashib ko'raman")
async def set_free_lesson_participant(message: Message, state: FSMContext):
    await db.survey_update_freeLessonParticipation(message.from_user.id, 'yes')
    await message.answer("Zo'r! Sizni shanba kuni soat 15:00 da bo'lib o'tadigan ochiq darsimizga yozib qo'ydim. O'zingiz bilan yaxshi kayfiyatni olib kelishingiz kifoya.",
                         reply_markup=await main_menu(telegramId=message.from_user.id))
    await state.clear()
    await message.delete()


@dp.message(StateFilter(Registration), PrivateFilter(), F.text == "❌ Yo'q, hozircha kerak emas")
async def set_free_lesson_participant_no(message: Message, state: FSMContext):
    await db.survey_update_freeLessonParticipation(message.from_user.id, 'no')
    await message.answer("So'rovnomada ishtirok etganingiz uchun rahmat!",
                         reply_markup=await main_menu(telegramId=message.from_user.id))
    await state.clear()
    await message.delete()
