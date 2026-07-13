from sqlalchemy import select

from database import SessionLocal
from .models import UserLocation


def get_user_location(user_id):
    query = select(UserLocation).where(
        UserLocation.user_id == user_id
    )
    with SessionLocal() as session:
        return session.scalar(query)


def create_location(location_kwargs):
    creation_kwargs = dict()
    for field in UserLocation.__table__.columns.keys():
        if (query_param := location_kwargs.get(field)):
            creation_kwargs[field] = query_param

    with SessionLocal() as session:
        location = UserLocation(**creation_kwargs)
        session.merge(location)
        session.commit()
    return location


def update_user_location(user_id, update_kwargs):
    user_location = get_user_location(user_id)
    if not user_location:
        raise KeyError('No user matches query.')

    for field in UserLocation.__table__.columns.keys():
        if (query_param := update_kwargs.get(field)):
            setattr(user_location, field, query_param)
