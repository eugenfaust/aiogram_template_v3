from abc import ABC
from typing import Any

from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

import config


class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.from_user.id in config.ADMIN_IDS:
            return True
        return False
