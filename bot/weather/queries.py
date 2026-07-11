from sqlalchemy import select

from database import SessionLocal
from .models import UserLocation


def create_location(creation_kwargs):
    creation_kwargs = dict()
    for field in UserLocation.__table__.columns.keys():
        if (query_param := creation_kwargs.get(field)):
            creation_kwargs[field] = query_param

    with SessionLocal() as session:
        task = UserLocation(**creation_kwargs)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def get_user_location(user_id):
    return select(UserLocation).where(
        UserLocation.user_id == user_id
    ).first()


def update_user_location(user_id, update_kwargs):
    user_location = get_user_location(user_id)
    if not user_location:
        raise KeyError('No user matches query.')

    for field in UserLocation.__table__.columns.keys():
        if (query_param := update_kwargs.get(field)):
            setattr(user_location, field, query_param)
