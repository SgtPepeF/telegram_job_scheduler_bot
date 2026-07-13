from .models import User
from . import SessionLocal


USER_REQUIRED_FIELDS = {'user_id', }
USER_OPTIONAL_FIELDS = {'username', }
USER_SEARCH_FIELDS = {'user_id', 'username', }


def get_user(user_kwargs):
    search_kwargs = dict()
    for search_field in USER_SEARCH_FIELDS:
        if (query_param := user_kwargs.get(search_field)):
            search_kwargs[search_field] = query_param

    if search_kwargs:
        with SessionLocal() as session:
            return session.query(User).filter_by(
                **search_kwargs
            ).first()
    raise KeyError('Wrong query params')


def create_user(user_kwargs):

    # check if user alredy exists:
    existing_user = get_user(user_kwargs)

    if existing_user:
        raise ValueError('User alredy exists.')

    creation_kwargs = dict()
    for required_field in USER_REQUIRED_FIELDS:
        if (query_param := user_kwargs.get(required_field)):
            creation_kwargs[required_field] = query_param

    if not creation_kwargs:
        raise ValueError('Missing required kwargs')

    for optional_field in USER_OPTIONAL_FIELDS:
        if (query_param := user_kwargs.get(optional_field)):
            creation_kwargs[optional_field] = query_param

    with SessionLocal() as session:
        user = User(**creation_kwargs)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def delete_user(user_kwargs):
    user = get_user(user_kwargs)
    with SessionLocal as session:
        session.delete(user)
        session.commit()
