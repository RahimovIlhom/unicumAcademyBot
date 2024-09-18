from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from environs import Env

from utils import Database

env = Env()
env.read_env()

bot = Bot(token=env.str('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
db = Database()


async def connect_database():
    await db.connect()


async def close_database():
    await db.close()
