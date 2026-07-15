
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

from . import (
    Base
)


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer(), primary_key=True)
