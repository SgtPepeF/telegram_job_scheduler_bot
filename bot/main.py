from datetime import datetime
import time
import sqlite3
import os

from dotenv import load_dotenv
import telebot

from weather.weather import forecast


load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', 'put your telegram token here or set its value in .env file')
ADMIN_ID = int(os.getenv('ADMIN_TELEGRAM_ID'))


COMMANDS = {
    '/start': 'Начать работу с ботом',
    '/time': 'Ответит текущим временем на сервере',
    '/forecast': 'Отправит текущую погоду в Перми.',
    '/register': 'Добавляет юзера в регулярную рассылку погоды.'
}


bot = telebot.TeleBot(API_TOKEN)


keyboard = telebot.types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
)

for command in COMMANDS:
    keyboard.add(
        telebot.types.KeyboardButton(command)
    )


# represented as a wrapper
def common_keyboard(func):
    def wrapper(*args, **kwargs):
        message, = args

        result = func(*args, **kwargs)

        bot.send_message(
            chat_id=message.chat.id,
            text='sended common keyboard.',
            reply_markup=keyboard
        )
        return result
    return wrapper


db_connection = sqlite3.connect('users.db', check_same_thread=False)
cursor = db_connection.cursor()

cursor.execute("""
    create table if not exists users (
        user_id integer primary key,
        username text,
        mailing_flg boolean default True
    )
""")
db_connection.commit()


def add_user(user):
    cursor.execute('''
        INSERT OR REPLACE INTO users
        (user_id, username)
        VALUES (?, ?)''', (
            user.id,
            user.username
        )
    )
    db_connection.commit()


@bot.message_handler(commands=['time'])
def echo_time(message):
    current_time = datetime.now()
    str_time = current_time.strftime(format='Время %H:%M:%S\nДата %d.%m.%Y')
    bot.reply_to(message, f'{str_time}')


@bot.message_handler(commands=['forecast'])
def get_forecats(message):
    text = forecast()

    bot.send_message(
        chat_id=message.from_user.id,
        text=text
    )


@bot.message_handler(commands=['register'])
def register_user(message):
    add_user(message.from_user)
    REPLY = f"""
    Пользователь @{message.from_user.username} успешно добавлен в рассылку погоды.
    """.replace('    ', '')
    bot.reply_to(message, REPLY)


# exclusive for @admin only
@bot.message_handler(
    commands=['forecast_for_registered'],
    func=lambda message: message.chat.id == ADMIN_ID
)
def send_forecast_for_subscribers(message):
    subscribers = cursor.execute("""
        select user_id
        from users
        ;
    """).fetchall()

    MESSAGE = forecast()
    for (subscriber,) in subscribers:
        time.sleep(.03)
        result = bot.send_message(subscriber, MESSAGE)
        print(result)

    bot.reply_to(message, 'Рассылка завершена.')


@bot.message_handler(content_types=('text',))
def common_reply(message):
    TEXT_REPLY = """Команда не распознана."""
    bot.reply_to(message, TEXT_REPLY)


if __name__ == '__main__':
    bot.infinity_polling()
