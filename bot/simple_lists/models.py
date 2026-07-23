from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, Integer, String,
    DateTime,
    func
)

from database import (
    Base
)


class UserList(Base):
    __tablename__ = 'user_list'

    list_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.user_id'),
    )
    list_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_dttm: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )


class ListsObject(Base):
    list_id: Mapped[int] = mapped_column(
        ForeignKey('user_list.list_id'),
    )
    object_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    created_dttm: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    comment: Mapped[str] = mapped_column(
        String,
    )
