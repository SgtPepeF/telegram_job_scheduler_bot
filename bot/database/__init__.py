from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from . import models

database_engine = create_engine('sqlite:///bot_database.db', echo=True)
