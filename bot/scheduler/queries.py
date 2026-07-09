from datetime import datetime

from sqlalchemy import (
    select,
)

from database import SessionLocal
from .models import Command


def create_task(creation_kwargs):
    creation_kwargs = dict()
    for field in Command.__table__.columns.keys():
        if (query_param := creation_kwargs.get(field)):
            creation_kwargs[field] = query_param

    with SessionLocal() as session:
        task = Command(**creation_kwargs)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def get_regular_tasks():
    return select(Command).where(
        Command.regular_task
    )


def get_actual_tasks():
    current_time = datetime.now()
    return select(Command).where(
        Command.execute_dttm >= current_time
    )
