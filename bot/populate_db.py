from datetime import datetime

from database import SessionLocal
from database.queries import create_user
from scheduler.queries import create_task

from settings import (
    ADMIN_TELEGRAM_ID,
    ADMIN_USERNAME,
)

REGULAR_TASK_TIME_FORMAT = '%H:%M'

session = SessionLocal()

# create admin user
try:
    create_user(
        user_kwargs={
            'username': ADMIN_USERNAME,
            'user_telegram_id': ADMIN_TELEGRAM_ID
        }
    )
except ValueError as user_exists:
    print(user_exists)
except KeyError as wrong_params:
    print(wrong_params)

time_to_send_forecast = [
    datetime.strptime('00:00', REGULAR_TASK_TIME_FORMAT),
    datetime.strptime('09:00', REGULAR_TASK_TIME_FORMAT),
    datetime.strptime('12:00', REGULAR_TASK_TIME_FORMAT),
    datetime.strptime('18:00', REGULAR_TASK_TIME_FORMAT),
]

for exec_time in time_to_send_forecast:
    create_task(
        kwargs={
            'author_id': ADMIN_TELEGRAM_ID,
            'regular_task': True,
            'execute_dttm': exec_time,
            'function': 'bot_send_forecat',
            'arguments': {'user_id': ADMIN_TELEGRAM_ID}
        }
    )


regular_messeges = [
    # [message, time]
    [
        'Полночь. Никакой больше работы!!! 🌙🌌',
        datetime.strptime('00:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'Good morning, World! 😎',
        datetime.strptime('08:59', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        'Полдень. Praise the SUN! 🔥☀️🌻',
        datetime.strptime('12:00', REGULAR_TASK_TIME_FORMAT),
    ],
    [
        '18:00 Рабочий день окончен. 🌈',
        datetime.strptime('18:00', REGULAR_TASK_TIME_FORMAT),
    ]
]

for message, exec_time in regular_messeges:
    create_task(
            kwargs={
                'author_id': ADMIN_TELEGRAM_ID,
                'regular_task': True,
                'execute_dttm': exec_time,
                'function': 'send_message',
                'arguments': {
                    'user_id': ADMIN_TELEGRAM_ID,
                    'text': message
                }
            }
        )
