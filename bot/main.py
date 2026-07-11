from telegram_bot.bot import telegtam_bot
from scheduler import scheduler

from set_up import set_up_schedule


if __name__ == '__main__':
    set_up_schedule()
    scheduler.start()
    telegtam_bot.infinity_polling()
