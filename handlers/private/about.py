from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message

from config.data import ABOUT_TEXT
from filters import PrivateFilter
from loader import dp, db


@dp.message(StateFilter(None), PrivateFilter(), F.text == "ℹ️ O'quv markaz haqida")
async def about(message: Message):
    await message.answer(ABOUT_TEXT)
