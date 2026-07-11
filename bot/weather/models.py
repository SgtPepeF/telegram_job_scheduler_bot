from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, String, JSON
)

from database import Base


class UserLocation(Base):
    __tablename__ = 'user_location'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        nullable=False,
        unique=True
    )
    location: Mapped[str] = mapped_column(
        String
    )
    lon_lat: Mapped[dict] = mapped_column(
        JSON
    )
