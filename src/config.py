import os
from os import getenv

from dotenv import load_dotenv

if not getenv('DEBUG'):
    load_dotenv()
else:
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".envtest")))


class CONFIG:
    BOT_API_TOKEN = getenv('BOT_API_TOKEN')
    DB_URI = getenv('DB_URI')
    SECRET_KEY = getenv('SECRET_KEY')
    USE_CONSOLE = getenv('USE_CONSOLE')
    APP_HOST = getenv('APP_HOST')
    TEST_APP_ID = getenv('TEST_APP_ID')
    TEST_APP_HASH = getenv('TEST_APP_HASH')
    DEBUG = getenv('DEBUG')


config = CONFIG()
