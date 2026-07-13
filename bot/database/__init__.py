from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import DEBUG_MODE


class Base(DeclarativeBase):

    def to_dict(self):
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self).mapper.column_attrs
        }


from . import models

database_engine = create_engine('sqlite:///bot_database.db', echo=DEBUG_MODE)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=database_engine
)

from . import queries
