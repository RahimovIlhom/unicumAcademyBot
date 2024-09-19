from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_contact_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📞 Kontaktni ulashish", request_contact=True)
            ],
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return contact_markup
