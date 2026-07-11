from .bot import telegtam_bot


from weather.weather import forecast


# Looks unnecessary, but now we can schedule messaging.
def send_message(user_id, text):
    telegtam_bot.send_message(
        chat_id=user_id,
        text=text
    )


def bot_send_forecat(user_id, city='perm'):
    """Sends a forecast to a chosen user."""
    TEXT_REPLY = forecast(city=city)
    send_message(user_id, TEXT_REPLY)


@telegtam_bot.message_handler(commands=('forecast', 'погода'))
def reply_forecast(message):
    return bot_send_forecat(
        user_id=message.from_user.id
    )


@telegtam_bot.message_handler(content_types=('text',))
def common_reply(message):
    TEXT_REPLY = """Команда не распознана."""
    telegtam_bot.reply_to(message, TEXT_REPLY)
