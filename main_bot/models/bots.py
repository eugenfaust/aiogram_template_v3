from sqlalchemy import sql, Column, BigInteger, String, Integer, Boolean, DateTime, ForeignKey

from .base import BaseModel


class UserBot(BaseModel):
    __tablename__ = 'bots'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    status = Column(Boolean, default=True)
    token = Column(String(50), unique=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created = Column(DateTime(timezone=True))