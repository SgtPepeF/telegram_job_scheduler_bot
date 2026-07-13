from copy import copy
from datetime import datetime
from re import fullmatch as regexp_fullmatch

from .constants import (
    DATETIME_FORMAT,
    DATE_REGEXP_FORMATS,
    TIME_REGEXP_FORMATS,
)
from .commands import (
    REGISTERED_BOT_COMMANDS
)


def check_formatting(string, allowed_formats):
    coincidences_map = [
        regexp_fullmatch(string=string, pattern=date_format)
        for date_format in allowed_formats
    ]
    return any(coincidences_map)


def parse_datetime_string(string, periods, sep=' ') -> dict:
    datetime_values = [
        int(number_str)
        for number_str in string.split(sep)
    ]
    return dict(
        zip(periods, datetime_values)
    )


def pop_first_word(string):
    splitted_string = string.split(' ', 1)
    # end of the line
    if len(splitted_string) < 2:
        splitted_string.append(None)
    return splitted_string


def parse_command(text_command) -> tuple:
    unparsed_command = copy(text_command)
    _, unparsed_command = pop_first_word(unparsed_command)
    current_argument, unparsed_command = pop_first_word(unparsed_command)
    # 1. Check if task is regular
    regular_task = False
    if current_argument in {'regular', 'регулярно'}:
        regular_task = True
        # Go to the next command word.
        current_argument, unparsed_command = pop_first_word(unparsed_command)

    parsed_datetime_args = dict()

    # 2. Check if current command argument is date.
    if check_formatting(current_argument, DATE_REGEXP_FORMATS):
        parsed_datetime_args |= parse_datetime_string(
            current_argument,
            periods=('day', 'month', 'year'),
            sep='.'
        )
        # Go to the next command word.
        current_argument, unparsed_command = pop_first_word(unparsed_command)

    # 2.1 Check if current command argument is time.
    if check_formatting(current_argument, TIME_REGEXP_FORMATS):
        parsed_datetime_args |= parse_datetime_string(
            current_argument,
            periods=('hour', 'minute'),
            sep=':'
        )
        current_argument, unparsed_command = pop_first_word(unparsed_command)

    current_time = datetime.now()

    # Merging current time with parsed_datetime to get full execute_time.
    execute_time_args = dict(
        [
            (period, getattr(current_time, period))
            for period in ('year', 'month', 'day', 'hour', 'minute')
        ]
    ) | parsed_datetime_args

    try:
        execute_dttm = datetime(**execute_time_args)
    except ValueError:
        raise ValueError(
            """
                Неправильный формат даты и времени.
                Команда поддерживает формат:
                /command [DD.MM.YYYY] [hh:mm] [action] ...
            """.replace('    ', '')
        )

    if execute_dttm < current_time:
        raise ValueError(
            f"""
                Попытка запланировать действие в прошлом.
                Действие запланировано на {execute_dttm.strftime(DATETIME_FORMAT)}
                Текущее время {current_time.strftime(DATETIME_FORMAT)}
                Формат даты и времени:
                /command [DD.MM.YYYY] [hh:mm] [action] ...
            """.replace('    ', '')
        )

    # 3 Read action.
    function = REGISTERED_BOT_COMMANDS.get(current_argument)
    if not function:
        raise ValueError(
            """
                Выбрано неправильное действие (action).
                Команда поддерживает формат:
                /command [DD.MM.YYYY] [hh:mm] [action] ...
            """.replace('    ', '')
        )

    return dict(
        regular_task=regular_task,
        execute_dttm=execute_dttm,
        function=function,
        argument=unparsed_command
    )
