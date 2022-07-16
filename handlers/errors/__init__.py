import logging
from typing import Any

from aiogram import Router, types
from aiogram.dispatcher.handler import ErrorHandler


def setup():
    router = Router()
    router.errors.register(MyHandler)
    return router


class MyHandler(ErrorHandler):
    async def handle(self) -> Any:
        print('error')
        await self.event.message.answer('Hello')
        logging.exception(
            "Cause unexpected exception %s: %s",
            self.exception_name,
            self.exception_message
        )
