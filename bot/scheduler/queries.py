from datetime import datetime

from sqlalchemy import (
    select,
)

from database import SessionLocal
from .models import Command


def get_task(task_id):
    with SessionLocal() as session:
        task = session.query(Command).filter_by(
            id=task_id
        ).first()
    return task


def create_task(kwargs):

    if (task_id := kwargs.get('id')):
        existing_task = get_task(task_id)
        if existing_task:
            raise ValueError('Task alredy exists.')

    creation_kwargs = dict()
    for field in Command.__table__.columns.keys():
        if (query_param := kwargs.get(field)):
            creation_kwargs[field] = query_param

    with SessionLocal() as session:
        task = Command(**creation_kwargs)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def get_regular_tasks():
    query = select(Command).where(
        Command.regular_task
    )
    with SessionLocal() as session:
        tasks = session.scalars(query).all()
    return tasks


def get_actual_tasks():
    current_time = datetime.now()
    query = select(Command).where(
        Command.execute_dttm >= current_time
    )
    with SessionLocal() as session:
        tasks = session.scalars(query).all()
    return tasks
