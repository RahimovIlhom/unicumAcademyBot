from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from environs import Env

env = Env()
env.read_env()


async def main_menu(telegramId, lang: str = 'uz') -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🧑‍💻 Test topshirish",
                    web_app=WebAppInfo(url=env.str('NGROK_URL').format(telegramId=telegramId))
                ),
            ],
            [
                KeyboardButton(text="ℹ️ Kurs haqida"),
                KeyboardButton(text="📝 Ma'lumotlarim"),
            ],
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="⚙️ Sozlamalar")
            ]
        ],
        resize_keyboard=True, row_width=2
    )
    return menu
