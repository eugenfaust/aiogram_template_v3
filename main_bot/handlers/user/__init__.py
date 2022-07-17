from aiogram import Router, F
from aiogram.dispatcher.filters import Command

from main_bot.filters import AdminFilter
from .add import bot_add, is_bot_token
from .help import bot_help
from .start import bot_start, clb_start


def setup():
    router = Router()
    router.message.register(bot_start, Command(commands='start'))
    router.message.register(bot_help, Command(commands='help'))
    router.callback_query.register(clb_start, F.data == 'hello', AdminFilter())
    router.message.register(bot_add, Command(commands='add', command_magic=F.args.func(is_bot_token)))
    return router
