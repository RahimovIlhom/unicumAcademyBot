import logging
import ssl
import sys

from aiohttp import web
from environs import Env

import middlewares, filters, handlers
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from loader import close_database, connect_database, dp, bot
from utils.set_bot_commands import set_default_commands

env = Env()
env.read_env()

WEB_SERVER_HOST = env.str('WEB_SERVER_HOST')
WEB_SERVER_PORT = env.int('WEB_SERVER_PORT')

WEBHOOK_PATH = env.str('WEBHOOK_PATH')
WEBHOOK_SECRET = env.str('WEBHOOK_SECRET')
BASE_WEBHOOK_URL = env.str('BASE_WEBHOOK_URL')

WEBHOOK_SSL_CERT = env.str('WEBHOOK_SSL_CERT')
WEBHOOK_SSL_PRIV = env.str('WEBHOOK_SSL_PRIV')


async def on_startup() -> None:
    await set_default_commands()
    await connect_database()
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(close_database)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context = ssl.create_default_context()
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, ssl_context=context)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
