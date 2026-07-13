from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, String, JSON
)

from database import Base


class UserLocation(Base):
    __tablename__ = 'user_location'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.user_id'),
        primary_key=True
    )
    location: Mapped[str] = mapped_column(
        String(50)
    )
    lon_lat: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )
