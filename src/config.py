from os import getenv

from dotenv import load_dotenv

load_dotenv()


class CONFIG:
    BOT_API_TOKEN = getenv('BOT_API_TOKEN')
    DB_URI = getenv('DB_URI')
    SECRET_KEY = getenv('SECRET_KEY')
    USE_CONSOLE = getenv('USE_CONSOLE')
    APP_HOST = getenv('APP_HOST')


config = CONFIG()
