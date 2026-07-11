from datetime import datetime, timedelta

from settings import ADMIN_TELEGRAM_ID

from scheduler.actions import (
    schedule_task,
)
from scheduler.queries import (
    get_actual_tasks,
    get_regular_tasks
)

from telegram_bot.commands import (
    send_message,
    bot_send_forecat
)


TASKS_MAP = {
    send_message.__name__: send_message,
    bot_send_forecat.__name__: bot_send_forecat,
}


def set_up_schedule():
    regular_tasks = get_regular_tasks()
    actual_tasks = get_actual_tasks()

    tasks = regular_tasks + actual_tasks

    for task in tasks:
        function_to_schedule = TASKS_MAP.get(task.function)
        if not function_to_schedule:
            print('No Task named task.function')
            continue
        schedule_task(
            function_to_schedule,
            execute_dttm=task.execute_dttm,
            arguments=task.arguments,
            regular_task=task.regular_task
        )

    # schedule greeting message.
    greeting_time = datetime.now() + timedelta(seconds=5)
    greeting_text = f"""
        Bot is up and running! 🤖🎶

        scheduled tasks 🗒:
        ┬ {len(tasks)} total
        ├ {len(regular_tasks)} regular
        └ {len(actual_tasks)} actual
    """.replace('    ', '')
    schedule_task(
        send_message,
        execute_dttm=greeting_time,
        arguments={
            'user_id': ADMIN_TELEGRAM_ID,
            'text': greeting_text
        },
        regular_task=False
    )
