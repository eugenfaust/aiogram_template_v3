from aiogram import types

from main_bot.keyboards.inline.menu import get_menu
from main_bot.models import User


async def bot_start(msg: types.Message, user: User):
    await msg.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())


async def clb_start(clb: types.CallbackQuery, user: User):
    await clb.answer()
    await clb.message.delete()
    await clb.message.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())