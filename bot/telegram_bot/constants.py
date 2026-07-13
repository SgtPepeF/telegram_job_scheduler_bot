DATETIME_FORMAT = '%H:%M %d.%m.%Y'

DATE_REGEXP_FORMATS = {
    r'\d{2}\.\d{2}',  # DD.MM
    r'\d{1}\.\d{2}',  # D.MM
    r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
    r'\d{1}\.\d{2}\.\d{4}',  # D.MM.YYYY
}

TIME_REGEXP_FORMATS = {
    r'\d{2}:\d{2}',  # hh:mm
}
