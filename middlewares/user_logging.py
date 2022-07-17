import datetime
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from models import User


class UserLoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user: User = await User.get(event.from_user.id)
        if not user:
            user = await User.create(id=event.from_user.id, full_name=event.from_user.full_name,
                                     username=event.from_user.username, created=datetime.datetime.now())
        data['user'] = user
        result = await handler(event, data)
        await User.update(event.from_user.id, last_action=datetime.datetime.now())
        return result
