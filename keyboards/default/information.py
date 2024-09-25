from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def information_edit_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    contact_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✏️ Ismni tahrirlash"),  # Qalam emoji
                KeyboardButton(text="📞 Raqamni tahrirlash")  # Telefon emoji
            ],
            [
                KeyboardButton(text="🕒 Kurs vaqtini tahrirlash"),  # Soat emoji
            ],
            [
                KeyboardButton(text="◀️ Orqaga qaytish"),  # Orqaga qaytish emoji
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    return contact_markup
