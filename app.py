import asyncio
import logging
import sys

import middlewares, filters, handlers
from loader import dp, bot, connect_database, close_database, db
from utils.set_bot_commands import set_default_commands


async def on_startup():
    await set_default_commands()
    await connect_database()


async def main():
    """
    Main bot runner. This will start the bot and handle setup.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.startup.register(on_startup)
    dp.shutdown.register(close_database)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
