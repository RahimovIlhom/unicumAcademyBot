from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import LEVELS


async def levels_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardBuilder()

    # Levellarni klaviaturaga qo'shish
    for level_name in LEVELS:
        contact_markup.add(KeyboardButton(text=level_name))

    return contact_markup.adjust(2).as_markup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
