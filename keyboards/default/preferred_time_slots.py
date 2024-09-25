from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def preferred_time_slots(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="09:00 dan 12:00 gacha"),
            ],
            [
                KeyboardButton(text="12:00 dan 15:00 gacha"),
            ],
            [
                KeyboardButton(text="15:00 dan 18:00 gacha"),
            ],
            [
                KeyboardButton(text="18:00 dan 21:00 gacha"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return contact_markup
