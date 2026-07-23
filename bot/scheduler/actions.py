from datetime import datetime, timezone, timedelta
from apscheduler.triggers.cron import CronTrigger

from . import scheduler
from .queries import get_user_timezone
from .constants import (
    DATETIME_FORMAT,
    TIME_FORMAT,
    SERVER_TIMEZONE
)


def schedule_task(
    function: str,
    execute_dttm: datetime,
    task_id: str = None,
    arguments: dict = None,
    regular_task: bool = False,
):
    if regular_task:
        trigger = CronTrigger(
            minute=execute_dttm.minute,
            hour=execute_dttm.hour,
        )
    else:
        trigger = 'date'

    return scheduler.add_job(
        id=task_id,
        func=function,
        trigger=trigger,
        run_date=execute_dttm,
        kwargs=arguments
    )


def unschedule_task(task_id: str):
    return scheduler.remove_job(task_id)


def get_task_text_representation(task):
    user_timedelta = get_user_server_timedelta(task.author_id)
    user_execution_time = task.execute_dttm + user_timedelta
    dttm_format = TIME_FORMAT if task.regular_task else DATETIME_FORMAT
    return f"""
        id задачи: {task.id}
        Регулярная: {'Да' if task.regular_task else 'Нет'}
        Будет исполнена:
        • {user_execution_time.strftime(dttm_format)} по времени пользователя;
        • {task.execute_dttm.strftime(dttm_format)} по времени сервера.
        Функция: {task.function}
        Содержание: {task.arguments.get('argument')}
    """.replace('    ', '')


def get_server_time():
    return datetime.now()


def get_utc_time():
    return datetime.now(timezone.utc)


def get_user_utc_timedelta(user_id):
    user_timezone = get_user_timezone(user_id)
    if not user_timezone:
        return SERVER_TIMEZONE
    return get_user_timezone(user_id).user_timezone


def get_user_server_timedelta(user_id):
    user_timezone = get_user_timezone(user_id)
    if not user_timezone:
        return timedelta(0)
    return user_timezone.user_server_timedelta


def get_user_time(user_id):
    user_timezone = get_user_timezone(user_id)
    if not user_timezone:
        return get_server_time()
    user_time = get_utc_time() + user_timezone.user_timezone
    return user_time
