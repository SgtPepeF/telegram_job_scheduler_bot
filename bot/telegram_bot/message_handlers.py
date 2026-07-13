from copy import copy
from datetime import datetime

from database.queries import create_user
from scheduler.queries import (
    create_task,
    get_task,
    get_user_tasks,
    delete_task
)
from weather.queries import create_location
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
    send_help,
)
from .utils import pop_first_word


@telegtam_bot.message_handler(commands=['start', 'старт'])
def start(message):

    user = create_user(
        user_kwargs={
            'user_id': message.from_user.id,
            'username': message.from_user.username
        }
    )  # rewrites username in case user exists.

    send_message(
        user.user_id,
        f'Приветствую, @{user.username}!'
    )

    return send_help(user.user_id)


@telegtam_bot.message_handler(commands=['help', 'помощь'])
def help(message):
    text_to_parse = copy(message.text)
    _, command_argument = pop_first_word(text_to_parse)
    return send_help(
        message.from_user.id,
        command_argument
    )


@telegtam_bot.message_handler(commands=['forecast', 'погода'])
def reply_forecast(message):
    text_to_parse = copy(message.text)
    _, command_argument = pop_first_word(text_to_parse)
    return send_forecat(
        user_id=message.from_user.id,
        argument=command_argument
    )


@telegtam_bot.message_handler(commands=['register', 'зарегистрировать'])
def register(message):
    text_to_parse = copy(message.text)
    _, text_to_parse = pop_first_word(text_to_parse)

    if not text_to_parse:
        return send_message(
            message.from_user.id,
            argument=(
                'Команда пуста.\n'
                'Попробуйте "/help register", если возникают трудности.'
            )
        )

    obj_to_reg, argument = pop_first_word(text_to_parse)

    full_actions_to_register = {'city', 'город', }

    if obj_to_reg not in full_actions_to_register:
        return send_message(
            message.from_user.id,
            f'Неизвестное действие {obj_to_reg}.'
        )

    if not argument or not argument.strip():
        return send_message(
            message.from_user.id,
            argument=(
                f'Недопустимый аргумент для действия {obj_to_reg}.'
                'Попробуйте "/help register", если возникают трудности.'
            )
        )

    if obj_to_reg in {'city', 'город'}:
        new_location = create_location(
            location_kwargs={
                'user_id': message.from_user.id,
                'location': argument.strip().capitalize()
            }
        )  # rewrites old location if exists

        return send_message(
            message.from_user.id,
            argument=(
                f'Новая локация успешно установлена: {new_location.location}.\n'
                'Обратите внимание, что бот не проверяет наличие ошибок в локации.'
                'Если локация написана с ошибкой ресурс Open Weather Map может'
                'вернуть статус 404.'
            )
        )
    return send_message(
        message.from_user.id,
        argument=(
            f'Недопустимый аргумент для действия {obj_to_reg}.\n'
            f'Попробуйте "/help register", если возникают трудности.'
        )
    )


@telegtam_bot.message_handler(commands=['plan', 'запланируй'])
def plan_action(message):
    try:
        command_arguments = parse_command(message.text)
    except ValueError as command_error:
        return send_message(
            user_id=message.from_user.id,
            argument=command_error
        )

    task = create_task(
        kwargs={
            'author_id': message.from_user.id,
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

    success_message = f"""
        ✅Задача успешно создана.
        id задачи: {task.id}
        Регулярная: {'Да' if task.regular_task else 'Нет'}
        Будет исполнена: {datetime.strftime(task.execute_dttm, DATETIME_FORMAT)}
        Функция: {task.function}
        Содержание: {task.arguments.get('argument')}

        Если вы хотите удалить задачу, воспользуйтесь командой
        /delete {task.id}
    """.replace('    ', '')

    send_message(
        message.from_user.id,
        success_message
    )


@telegtam_bot.message_handler(commands=['tasks', 'задачи'])
def list_actions(message):
    tasks = get_user_tasks(message.from_user.id)
    if not tasks:
        send_message(
            message.from_user.id,
            'У Вас нет запланированных задач.'
        )
    reply_text = f'У Вас {len(tasks)} запланированных задач:'
    for task in tasks:
        reply_text += f"""

            Задача id_{task.id}:
            Регулярная: {'Да' if task.regular_task else 'Нет'}
            Запланирована на {datetime.strftime(task.execute_dttm, DATETIME_FORMAT)}
            Функция: {task.function}
            Содержание: {task.arguments.get('argument')}
        """
    reply_text = reply_text.replace('    ', '')
    send_message(
        message.from_user.id,
        reply_text
    )


@telegtam_bot.message_handler(commands=['delete', 'удалить'])
def delete_action(message):
    text_to_parse = copy(message.text)
    _, task_id = pop_first_word(text_to_parse)

    if not task_id:
        return send_message(
            message.from_user.id,
            argument=(
                'Команда пуста.\n'
                'Попробуйте "/help delete", если возникают трудности.'
            )
        )
    try:
        task_id = int(task_id)
    except ValueError:
        return send_message(
            message.from_user.id,
            argument=(
                'id должен быть целым числом.\n'
                'Попробуйте "/help delete", если возникают трудности.'
            )
        )

    task = get_task(task_id)
    if not task:
        return send_message(
            message.from_user.id,
            argument=(
                'Задачи с указанным id не существует.'
            )
        )
    if task.author_id != message.from_user.id:
        return send_message(
            message.from_user.id,
            argument=(
                'Это не Ваша задача. Задачу может удалить только её автор.'
            )
        )
    delete_task(task_id)
    return send_message(
        message.from_user.id,
        argument=(
            f'Задача {task_id} успешно удалена🗑.'
        )
    )


@telegtam_bot.message_handler(content_types=['text'])
def common_reply(message):
    TEXT_REPLY = """Команда не распознана."""
    telegtam_bot.reply_to(message, TEXT_REPLY)
