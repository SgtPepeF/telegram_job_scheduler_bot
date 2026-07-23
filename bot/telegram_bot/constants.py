from datetime import timedelta

DATETIME_FORMAT = '%H:%M %d.%m.%Y'
TIME_FORMAT = '%H:%M'
LONG_TIME_FORMAT = '%H часов %M минут'

DATE_REGEXP_FORMATS = {
    r'\d{2}\.\d{2}',  # DD.MM
    r'\d{1}\.\d{2}',  # D.MM
    r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
    r'\d{1}\.\d{2}\.\d{4}',  # D.MM.YYYY
}

TIME_REGEXP_FORMATS = {
    r'\d{2}:\d{2}',  # hh:mm
}


DEFAULT_WORK_TIME = timedelta(minutes=50)
DEFAULT_REST_TIME = timedelta(minutes=10)
DEFAULT_AWAIT_TIME = timedelta(minutes=5)
