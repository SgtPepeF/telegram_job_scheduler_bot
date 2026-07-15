
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, Integer, String,
    DateTime, Interval, JSON, Boolean,
    func
)

from database import (
    Base
)
from .constants import (
    SERVER_TIMEZONE,
)


class Command(Base):
    __tablename__ = 'command'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    created_dttm: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    updated_dttm: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('user.user_id')
    )
    regular_task: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    execute_dttm: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    function: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    arguments: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )


class UserTimezone(Base):
    __tablename__ = 'user_timezone'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.user_id'),
        primary_key=True
    )
    user_timezone: Mapped[timedelta] = mapped_column(
        Interval,
        default=SERVER_TIMEZONE
    )
    user_server_timedelta: Mapped[timedelta] = mapped_column(
        Interval,
        default=timedelta(0)
    )
