from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import PrivateFilter
from keyboards.default import main_menu
from loader import dp


@dp.message(StateFilter(None), PrivateFilter(), F.text == "◀️ Orqaga qaytish")
async def back_to_main_menu(message: Message):
    await message.answer("Bosh menyu", reply_markup=await main_menu(telegramId=message.from_user.id))
