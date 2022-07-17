from aiogram import Bot, Dispatcher

from bot import main_dispatcher, ai_bot
from models.database import init_db


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook()
    await init_db()


if __name__ == "__main__":
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.run_polling(ai_bot)
