from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from environs import Env

env = Env()
env.read_env()


async def registered_types(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📋 So'rovnomada ishtirok etish",
                    web_app=WebAppInfo(url=env.str('SURVEY_URL'))
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
