from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyResultCallbackData(CallbackData, prefix='test_session'):
    test_session_id: int
    level: int


async def make_callback_data(test_session_id: int, level: int = 0) -> str:
    return MyResultCallbackData(test_session_id=test_session_id, level=level).pack()


async def my_results_markup(results: list, lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    markup_builder = InlineKeyboardBuilder()
    n = len(results)

    for result in results:
        markup_builder.row(
            InlineKeyboardButton(
                text=f"{n}-test natijam",
                callback_data=await make_callback_data(result['id'], CURRENT_LEVEL + 1)
            )
        )
        n -= 1
    markup_builder.row(
        InlineKeyboardButton(
            text="❌ Xabarni yopish",
            callback_data=await make_callback_data(0, CURRENT_LEVEL - 1)
        )
    )

    return markup_builder.as_markup()


async def one_my_result_markup(lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup_builder = InlineKeyboardBuilder()
    markup_builder.row(
        InlineKeyboardButton(
            text="◀️ Orqaga qaytish",
            callback_data=await make_callback_data(0, CURRENT_LEVEL - 1)
        )
    )
    return markup_builder.as_markup()
