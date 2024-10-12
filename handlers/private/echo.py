from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from filters import PrivateFilter
from handlers.private.registration import start_registration
from keyboards.default import main_menu, registered_types
from loader import dp, db


@dp.message(StateFilter(None), PrivateFilter(), F.text == "◀️ Orqaga qaytish")
async def back_to_main_menu(message: Message):
    await message.answer("Bosh menyu", reply_markup=await main_menu(telegramId=message.from_user.id))


@dp.message(StateFilter(State(None)), PrivateFilter(), F.text)
async def echo(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        await start_registration(message, state)
    else:
        if user.get('status') == 'draft':
            await message.answer(
                f"Hurmatli {user.get('fullname')}! Unicum Academy'da ingliz tili kurslariga yozilmoqchimisiz yoki so'rovnomada ishtirok etmoqchimisiz?",
                reply_markup=await registered_types(message.from_user.id)
            )
            await state.clear()
            return
        # await message.answer("Bosh menyu", reply_markup=await main_menu(telegramId=message.from_user.id))
        # await state.clear()