import logging

from aiogram import types

from keyboards.inline.menu import get_menu


async def bot_start(msg: types.Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=get_menu())


async def clb_start(clb: types.CallbackQuery):
    logging.info('Handler clb_start')
    await clb.answer('HELLLOOOOOOO')
    await clb.message.delete()
    await clb.message.answer('Hello!!!!!', reply_markup=get_menu())