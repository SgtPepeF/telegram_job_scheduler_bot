from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


from . import models

database_engine = create_engine('sqlite:///bot_database.db', echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=database_engine
)

from . import queries
