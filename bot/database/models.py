
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from . import (
    Base
)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    user_telegram_id: Mapped[int] = mapped_column(Integer(), unique=True, nullable=False)
