import asyncio
import logging
import sys

import handlers, keyboards, middlewares, filters
from loader import dp, bot, connect_database, close_database, db


async def main():
    """
    Main bot runner. This will start the bot and handle setup.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.startup.register(connect_database)
    dp.shutdown.register(close_database)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
