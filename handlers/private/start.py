from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import PrivateFilter
from handlers.private.registration import start_registration
from keyboards.default import main_manu
from loader import dp, db


@dp.message(PrivateFilter(), CommandStart())
async def command_start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        await start_registration(message, state)
    else:
        await message.answer("Bosh menyu", reply_markup=await main_manu(lang=user['language']))
        await state.clear()
