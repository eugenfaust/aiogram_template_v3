from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, TokenBasedRequestHandler, setup_application
from aiohttp import web

import config
from main_bot.filters import AdminFilter
from main_bot.handlers import user as main_user, errors as main_errors
from child_bot.handlers import user as child_user, errors as child_errors
from main_bot.middlewares.user_logging import UserLoggingMiddleware
from main_bot.models.base import start_db, shutdown_db
from child_bot.models.base import start_db as child_start_db, shutdown_db as child_shutdown_db


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await start_db()
    await bot.set_webhook(f"{config.BASE_URL}{config.MAIN_BOT_PATH}")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await shutdown_db()


async def child_on_startup(dispatcher: Dispatcher, bot: Bot):
    await child_start_db()
    await bot.set_webhook(f"{config.BASE_URL}{config.MAIN_BOT_PATH}")


async def child_on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await child_shutdown_db()


def main():
    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": "HTML"}
    ai_bot = Bot(token=config.MAIN_BOT_TOKEN, **bot_settings)
    # storage = RedisStorage.from_url(REDIS_DSN, key_builder=DefaultKeyBuilder(with_bot_id=True))
    storage = MemoryStorage()

    main_dispatcher = Dispatcher(storage=storage)
    multibot_dispatcher = Dispatcher(storage=storage)
    # MAIN BOT
    # filters
    main_dispatcher.message.bind_filter(AdminFilter)
    main_dispatcher.callback_query.bind_filter(AdminFilter)
    # middlewares
    main_dispatcher.message.middleware(UserLoggingMiddleware())
    main_dispatcher.callback_query.middleware(UserLoggingMiddleware())
    # routers
    main_dispatcher.include_router(main_errors.setup())
    main_dispatcher.include_router(main_user.setup())
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.shutdown.register(on_shutdown)

    # CHILD BOT
    multibot_dispatcher.include_router(child_user.setup())
    multibot_dispatcher.include_router(child_errors.setup())
    # filters
    multibot_dispatcher.message.bind_filter(AdminFilter)
    multibot_dispatcher.callback_query.bind_filter(AdminFilter)
    # middlewares
    multibot_dispatcher.message.middleware(UserLoggingMiddleware())
    multibot_dispatcher.callback_query.middleware(UserLoggingMiddleware())
    # routers
    multibot_dispatcher.include_router(main_errors.setup())
    multibot_dispatcher.include_router(main_user.setup())
    multibot_dispatcher.startup.register(on_startup)
    multibot_dispatcher.shutdown.register(on_shutdown)


    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=ai_bot).register(app, path=config.MAIN_BOT_PATH)
    TokenBasedRequestHandler(
        dispatcher=multibot_dispatcher,
        bot_settings=bot_settings,
    ).register(app, path=config.OTHER_BOTS_PATH)
    setup_application(app, main_dispatcher, bot=ai_bot)
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
