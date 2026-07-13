"""File containing bot commands.

Note that EVERY bot command should have only 2 arguments:
    - user_telegtam_id for user to send message to
    - another STRING argument

every function must be registered to be used.
"""

from weather.queries import get_user_location
from weather.weather import forecast

from .bot import telegtam_bot


# Looks unnecessary, but with it can schedule messaging.
def send_message(user_id, argument):
    telegtam_bot.send_message(
        chat_id=user_id,
        text=argument
    )


def send_forecat(user_id, argument='perm'):
    """Sends a forecast to a chosen user."""
    if not argument:
        argument = get_user_location(user_id)
    TEXT_REPLY = forecast(city=argument)
    send_message(user_id, TEXT_REPLY)


def send_help(user_id, argument=None):
    HELP_TEXT = f"""
    Я -- бот-планировщик Ваших задач🤖⏱️

    Возможности бота:
     • Прогноз погоды по запросу;
     • Запланировать разовое/регулярное сообщение;
     • Запланировать разовое/регулярное действие из списка доступных действий бота.
     • Трекер рабочего времени (в разработке).

    

    Доступные команды:
    """.replace('    ','')
    send_message(user_id, HELP_TEXT)


REGISTERED_BOT_COMMANDS = {
    send_message.__name__: send_message,
    'message': send_message,
    'сообщение': send_message,
    send_forecat.__name__: send_forecat,
    'forecast': send_forecat,
    'погода': send_forecat,
    'прогноз': send_forecat,
}
