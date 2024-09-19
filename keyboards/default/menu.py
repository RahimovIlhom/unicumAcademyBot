from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_manu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧑‍💻 Test boshlash"),
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
