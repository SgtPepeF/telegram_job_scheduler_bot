import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', 'put your telegram token here or set its value in .env file')
ADMIN_TELEGRAM_ID = int(os.getenv('ADMIN_TELEGRAM_ID'))
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')

OPEN_WEATHER_API_TOKEN = os.getenv(
    'OPEN_WEATHER_API_TOKEN',
    'put your OpenWeatherMap token here or set its value in .env file.'
)

REGISTERED_APPS = (
    'database',
    'scheduler',
)
