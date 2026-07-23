from datetime import datetime, timedelta

from telebot import types

from scheduler.actions import (
    schedule_task,
    unschedule_task,
    get_user_time
)

from .constants import (
    TIME_FORMAT,
    DEFAULT_WORK_TIME,
    DEFAULT_REST_TIME,
    DEFAULT_AWAIT_TIME
)

from .bot import telegtam_bot
from .commands import send_message


@telegtam_bot.message_handler(commands=['work', 'работа'])
def work_mode(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Завершить работу 😴',
            callback_data='end_of_work'
        )
    )

    user_id = message.from_user.id

    user_dttm = get_user_time(user_id)
    work_time = DEFAULT_WORK_TIME
    server_rest_dttm = datetime.now() + work_time
    user_rest_dttm = user_dttm + work_time
    rest_time = DEFAULT_REST_TIME

    start_work_message = f"""
        Продуктивной Вам 🤖Р0b0┬bI👾🛸!
        Перерыв запланирован на {user_rest_dttm.strftime(TIME_FORMAT)}⏱️.
    """.replace('    ', '')

    message = telegtam_bot.send_message(
        user_id,
        start_work_message,
        reply_markup=markup
    )
    schedule_task(
        initialize_rest,
        server_rest_dttm,
        task_id=f'job_{user_id}',
        arguments={
            'user_id': user_id,
            'rest_time': rest_time,
            'init_message_id': message.message_id
        }
    )


def initialize_rest(user_id, init_message_id, rest_time: timedelta):
    # disable command markup from initial message
    telegtam_bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=init_message_id,
        reply_markup=None
    )

    rest_end = datetime.now() + rest_time
    user_rest_end = get_user_time(user_id) + rest_time

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='☀️ Принять перерыв',
            callback_data='accept_rest'
        ),
        types.InlineKeyboardButton(
            text='Завершить работу 😴',
            callback_data='end_of_work_mid_rest'
        )
    )

    rest_message = f"""
        🌻 Время для перерыва! 🌈

        Примите это сообщение до {user_rest_end.strftime(TIME_FORMAT)}⏱️.
    """.replace('    ', '')

    message = telegtam_bot.send_message(
        user_id,
        rest_message,
        reply_markup=markup
    )
    schedule_task(
        unanswered_rest,
        rest_end,
        task_id=f'job_{user_id}',
        arguments={
            'user_id': user_id,
            'init_message_id': message.message_id
        }
    )


def unanswered_rest(user_id, init_message_id):
    # delete callback message.
    telegtam_bot.delete_message(
        chat_id=user_id,
        message_id=init_message_id
    )
    return send_message(
        user_id,
        argument="""
            Вы не приняли перерыв.🛠
            ⚡️Работа завершена!⚡️
        """.replace('    ', '')
    )


@telegtam_bot.callback_query_handler(
    func=lambda call: call.data == 'accept_rest'
)
def callback_accept_rest(call):
    user_id = call.message.chat.id
    unschedule_task(f'job_{user_id}')

    telegtam_bot.answer_callback_query(
        call.id,
        '🧙🌿Время отдыхать!🌱🌳'
    )

    telegtam_bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    user_id = call.message.chat.id
    await_time = DEFAULT_AWAIT_TIME
    rest_time = DEFAULT_REST_TIME
    server_rest_end_dttm = datetime.now() + rest_time
    user_rest_end_dttm = get_user_time(user_id) + rest_time

    schedule_task(
        initialize_work,
        server_rest_end_dttm,
        task_id=f'job_{user_id}',
        arguments={
            'user_id': user_id,
            'await_time': await_time
        }
    )
    rest_message = f"""
        ⏳Начало перерыва!
        Перерыв продлится до {user_rest_end_dttm.strftime(TIME_FORMAT)}⏱️.
    """.replace('    ', '')
    return telegtam_bot.send_message(
        user_id,
        rest_message
    )


def initialize_work(user_id, await_time: timedelta):

    callback_await_end = datetime.now() + await_time
    user_rest_end = get_user_time(user_id) + await_time

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='🚀 Продолжить работу',
            callback_data='accept_work'
        ),
        types.InlineKeyboardButton(
            text='Завершить работу 😴',
            callback_data='end_of_work_mid_rest'
        )
    )

    rest_message = f"""
        ⌛️Перерыв окончен!🚀
        Пора возвращаться к работе!💻

        ❗️Примите это сообщение до {user_rest_end.strftime(TIME_FORMAT)}.
    """.replace('    ', '')

    message = telegtam_bot.send_message(
        user_id,
        rest_message,
        reply_markup=markup
    )
    schedule_task(
        unanswered_work,
        callback_await_end,
        task_id=f'job_{user_id}',
        arguments={
            'user_id': user_id,
            'init_message_id': message.message_id
        }
    )


def unanswered_work(user_id, init_message_id):
    # disable command markup from init rest message
    telegtam_bot.delete_message(
        chat_id=user_id,
        message_id=init_message_id
    )
    return send_message(
        user_id,
        argument="""
            Вы не приняли начало работы.🛠
            ⚡️Работа завершена!⚡️
        """.replace('    ', '')
    )


@telegtam_bot.callback_query_handler(
    func=lambda call: call.data == 'accept_work'
)
def callback_accept_work(call):
    user_id = call.message.chat.id
    unschedule_task(f'job_{user_id}')

    telegtam_bot.answer_callback_query(
        call.id,
        'Работаем!✏️📚🤓'
    )
    telegtam_bot.delete_message(
        chat_id=user_id,
        message_id=call.message.message_id
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Завершить работу',
            callback_data='end_of_work'
        )
    )

    user_dttm = get_user_time(user_id)
    work_time = DEFAULT_WORK_TIME
    server_rest_dttm = datetime.now() + work_time
    user_rest_dttm = user_dttm + work_time

    start_work_message = f"""
        Продолжаем работать!✏️📚
        Перерыв запланирован на {user_rest_dttm.strftime(TIME_FORMAT)}.
    """.replace('    ', '')

    message = telegtam_bot.send_message(
        user_id,
        start_work_message,
        reply_markup=markup
    )
    schedule_task(
        initialize_rest,
        server_rest_dttm,
        task_id=f'job_{user_id}',
        arguments={
            'user_id': user_id,
            'rest_time': DEFAULT_REST_TIME,
            'init_message_id': message.message_id
        }
    )


@telegtam_bot.callback_query_handler(
    func=lambda call: call.data == 'end_of_work'
)
def callback_end_work(call):
    user_id = call.message.chat.id
    unschedule_task(f'job_{user_id}')

    telegtam_bot.answer_callback_query(
        call.id,
        '👾 Работа завершена! 🤖'
    )
    telegtam_bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    return send_message(
        user_id,
        argument="""
            Конец работе!🥳
        """.replace('    ', '')
    )


@telegtam_bot.callback_query_handler(
    func=lambda call: call.data == 'end_of_work_mid_rest'
)
def callback_end_work_mid_rest(call):
    user_id = call.message.chat.id
    unschedule_task(f'job_{user_id}')

    telegtam_bot.answer_callback_query(
        call.id,
        '👾 Работа завершена! 🤖'
    )
    telegtam_bot.delete_message(
        chat_id=user_id,
        message_id=call.message.message_id
    )

    return send_message(
        user_id,
        argument="""
            Конец работе!🥳
        """.replace('    ', '')
    )
