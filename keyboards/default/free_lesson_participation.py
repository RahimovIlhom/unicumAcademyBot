from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


async def free_lesson_participation(lang: str = 'uz') -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="✅ Ha, bepul ochiq darsga qatnashib ko'raman"
                )
            ],
            [
                KeyboardButton(
                    text="❌ Yo'q, hozircha kerak emas"
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return markup
