from sqlalchemy import sql, Column, BigInteger, String, Integer, Boolean, DateTime

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    status = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    last_action = Column(DateTime(timezone=True))
    username = Column(String(50))
    created = Column(DateTime(timezone=True))