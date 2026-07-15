from datetime import datetime

SERVER_TIMEZONE = datetime.now().astimezone().utcoffset()

DATETIME_FORMAT = '%H:%M %d.%m.%Y'
TIME_FORMAT = '%H:%M'
