import importlib

from database import Base
from database import database_engine
from settings import REGISTERED_APPS


def register_models():
    for app in REGISTERED_APPS:
        try:
            importlib.import_module(f'{app}.models')
        except ModuleNotFoundError:
            pass
    Base.metadata.create_all(bind=database_engine)


if __name__ == "__main__":

    register_models()
