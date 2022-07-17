import logging
from os import getenv
from typing import Any, Dict, Union

from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiohttp import web

from filters import AdminFilter
from handlers import errors
from handlers import user
import config
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.filters import Command, CommandObject
from aiogram.dispatcher.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.dispatcher.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import Message
from models.base import start_db, shutdown_db
from middlewares.counter import CountMiddleware


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await start_db()
    await bot.set_webhook(f"{config.BASE_URL}{config.MAIN_BOT_PATH}")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await shutdown_db()


def main():
    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": "HTML"}
    bot = Bot(token=config.MAIN_BOT_TOKEN, **bot_settings)
    # storage = RedisStorage.from_url(REDIS_DSN, key_builder=DefaultKeyBuilder(with_bot_id=True))
    storage = MemoryStorage()

    main_dispatcher = Dispatcher(storage=storage)
    # filters
    main_dispatcher.message.bind_filter(AdminFilter)
    main_dispatcher.callback_query.bind_filter(AdminFilter)
    # middlewares
    main_dispatcher.message.middleware(CountMiddleware())
    main_dispatcher.callback_query.middleware(CountMiddleware())

    # routers
    main_dispatcher.include_router(errors.setup())
    main_dispatcher.include_router(user.setup())

    main_dispatcher.startup.register(on_startup)
    main_dispatcher.shutdown.register(on_startup)
    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot).register(app, path=config.MAIN_BOT_PATH)
    setup_application(app, main_dispatcher, bot=bot)
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(filename='bot.log', level=logging.DEBUG)
    main()