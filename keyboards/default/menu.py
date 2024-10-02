from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from environs import Env

env = Env()
env.read_env()


async def main_menu(telegramId, lang: str = 'uz') -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Ma'lumotlarim"),
                KeyboardButton(text="📊 Mening natijam"),
            ],
            [
                KeyboardButton(text="ℹ️ O'quv markaz haqida"),
            ]
        ],
        resize_keyboard=True, row_width=2
    )
    return menu
