from datetime import datetime

from sqlalchemy import (
    select, or_
)

from database import SessionLocal
from .models import Command, UserTimezone
from .constants import SERVER_TIMEZONE


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


def delete_task(task_id):
    user = get_task(task_id)
    with SessionLocal() as session:
        session.delete(user)
        session.commit()


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


def get_user_tasks(author_id):
    current_time = datetime.now()

    query = select(
        Command
    ).where(
        Command.author_id == author_id
    ).where(
        or_(
            Command.execute_dttm >= current_time,
            Command.regular_task
        )
    ).order_by(
        Command.execute_dttm
    )
    with SessionLocal() as session:
        tasks = session.scalars(query).all()
    return tasks


def get_user_timezone(user_id):
    with SessionLocal() as session:
        user_timezone = session.query(UserTimezone).filter_by(
            user_id=user_id
        ).first()
    return user_timezone


def create_user_timezone(user_id, user_timedelta):
    with SessionLocal() as session:
        user_server_timedelta = user_timedelta - SERVER_TIMEZONE
        timezone = UserTimezone(
            user_id=user_id,
            user_timezone=user_timedelta,
            user_server_timedelta=user_server_timedelta
        )
        session.merge(timezone)
        session.commit()
    return timezone
