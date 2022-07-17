import datetime
from typing import Union, Dict, Any

from aiogram import types, Bot
from aiogram.dispatcher.filters import CommandObject
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.utils.token import validate_token, TokenValidationError

import config
from main_bot.keyboards.inline.menu import get_menu
from main_bot.models import User
from main_bot.models import UserBot



def is_bot_token(value: str) -> Union[bool, Dict[str, Any]]:
    try:
        validate_token(value)
    except TokenValidationError:
        return False
    return True


async def bot_add(msg: types.Message, user: User, command: CommandObject, bot: Bot):
    user_bot = await UserBot.query.where(UserBot.token == command.args).gino.first()
    if user_bot:
        return msg.answer('Бот уже добавлен')
    new_bot = Bot(token=command.args, session=bot.session)
    try:
        bot_user = await new_bot.get_me()
    except TelegramUnauthorizedError:
        return msg.answer("Invalid token")
    await new_bot.delete_webhook(drop_pending_updates=True)
    await new_bot.set_webhook(config.OTHER_BOTS_URL.format(bot_token=command.args))
    await UserBot.create(token=command.args, user_id=user.id, created=datetime.datetime.now())
    await msg.answer(f"Bot @{bot_user.username} successful added")
    await msg.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())


async def clb_start(clb: types.CallbackQuery, user: User):
    await clb.answer()
    await clb.message.delete()
    await clb.message.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())