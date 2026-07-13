from datetime import datetime

from database.queries import get_user, create_user
from scheduler.queries import create_task
from scheduler.actions import schedule_task

from .constants import (
    DATETIME_FORMAT,
)
from .bot import telegtam_bot
from .utils import (
    parse_command,
)
from .commands import (
    send_message,
    send_forecat,
)
'user_id', 'username'

@telegtam_bot.message_handler(commands=['start', 'старт'])
def start(message):
    try:
        user = create_user(
            user_kwargs={
                'user_id': message.from_user.id,
                'username': message.from_user.username
            }
        )
    except ValueError as user_exists_error:
        pass
    
    send_message(
        user.user_id,
        f'Приветствую, @{user.username}!'
    )

    return send_message(
        user.user_id,
        GREETING_TEXT
    )


@telegtam_bot.message_handler(commands=['forecast', 'погода'])
def reply_forecast(message):
    return send_forecat(
        user_id=message.from_user.id
    )


@telegtam_bot.message_handler(commands=['plan', 'запланируй'])
def plan_action(message):
    try:
        command_arguments = parse_command(message.text)
    except ValueError as command_error:
        send_message(
            user_id=message.from_user.id,
            argument=command_error
        )
        return None

    user = get_user(
        user_kwargs={
            'user_id': message.from_user.id
        }
    )

    task = create_task(
        kwargs={
            'author_id': user.user_id,
            'regular_task': command_arguments.get('regular_task'),
            'execute_dttm': command_arguments.get('execute_dttm'),
            'function': (command_arguments.get('function')).__name__,
            'arguments': {
                'user_id': message.from_user.id,
                'argument': command_arguments.get('argument'),
            }
        }
    )

    schedule_task(
        function=command_arguments.get('function'),
        execute_dttm=task.execute_dttm,
        arguments=task.arguments,
        regular_task=task.regular_task,
    )


@telegtam_bot.message_handler(content_types=['text'])
def common_reply(message):
    TEXT_REPLY = """Команда не распознана."""
    telegtam_bot.reply_to(message, TEXT_REPLY)
