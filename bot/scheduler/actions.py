from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from . import scheduler


def schedule_task(
    function: str,
    execute_dttm: datetime,
    arguments: dict = None,
    regular_task: bool = False,
):
    if not regular_task:
        return scheduler.add_job(
            func=function,
            trigger='date',
            run_date=execute_dttm,
            kwargs=arguments
        )

    cron_trigger = CronTrigger(
        minute=execute_dttm.minute,
        hour=execute_dttm.hour,
    )
    return scheduler.add_job(
        func=function,
        trigger=cron_trigger,
        run_date=execute_dttm,
        kwargs=arguments
    )
