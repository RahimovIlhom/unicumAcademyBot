from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


async def registered_types(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📋 So'rovnomada ishtirok etish",
                    web_app=WebAppInfo(url="https://unicalm.uz/quiz")
                )
            ],
            [
                KeyboardButton(text="📝 Ro'yxatdan o'tish")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return contact_markup
