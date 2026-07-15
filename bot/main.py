from db_creation import register_models
from telegram_bot.bot import telegtam_bot
from scheduler import scheduler

from set_up import set_up_schedule


if __name__ == '__main__':
    register_models()
    set_up_schedule()
    scheduler.start()
    telegtam_bot.infinity_polling()
