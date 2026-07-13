from datetime import datetime

from database import SessionLocal
from database.queries import create_user
from scheduler.queries import create_task
from weather.queries import create_location

from settings import (
    ADMIN_TELEGRAM_ID,
    ADMIN_USERNAME,
    DEFAULT_OPENWEATHER_REGION,
)

REGULAR_TASK_TIME_FORMAT = '%H:%M'

session = SessionLocal()

# create admin user
try:
    create_user(
        user_kwargs={
            'user_id': ADMIN_TELEGRAM_ID,
            'username': ADMIN_USERNAME,
        }
    )
except ValueError as user_exists:
    print(user_exists)
except KeyError as wrong_params:
    print(wrong_params)

# determine admin user region
# create admin user
try:
    create_location(
        location_kwargs={
            'user_id': ADMIN_TELEGRAM_ID,
            'location': DEFAULT_OPENWEATHER_REGION,
        }
    )
except ValueError as location_exists:
    print(location_exists)
except KeyError as wrong_params:
    print(wrong_params)


task_to_schedule = [
    # [task, regular_flg, argument, execute_time]
    [
        'send_message',
        True,
        'Полночь. Никакой больше работы!!! 🌙🌌',
        datetime.strptime('00:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_message',
        True,
        'Good morning, World! 😎',
        datetime.strptime('08:59', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_message',
        True,
        'Полдень. Praise the SUN! 🔥☀️🌻',
        datetime.strptime('12:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_message',
        True,
        '18:00 Рабочий день окончен. 🌈',
        datetime.strptime('18:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_forecat',
        True,
        DEFAULT_OPENWEATHER_REGION,
        datetime.strptime('00:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_forecat',
        True,
        DEFAULT_OPENWEATHER_REGION,
        datetime.strptime('09:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_forecat',
        True,
        DEFAULT_OPENWEATHER_REGION,
        datetime.strptime('12:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'send_forecat',
        True,
        DEFAULT_OPENWEATHER_REGION,
        datetime.strptime('18:00', REGULAR_TASK_TIME_FORMAT),
    ]
]


for task_index in range(len(task_to_schedule)):
    task, regular_flg, argument, execute_time = task_to_schedule[task_index]
    try:
        create_task(
            kwargs={
                'id': task_index + 1,
                'author_id': ADMIN_TELEGRAM_ID,
                'regular_task': regular_flg,
                'execute_dttm': execute_time,
                'function': task,
                'arguments': {
                    'user_id': ADMIN_TELEGRAM_ID,
                    'argument': argument
                }
            }
        )
    except ValueError as user_exists:
        print(user_exists)
    except KeyError as wrong_params:
        print(wrong_params)
