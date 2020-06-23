import telebot
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from src.models import Teams
from src.bot.handlers import bot
from src.config import config
from src.extensions import session
from src.logger import create_logger

admin = Admin(name='microblog', template_mode='bootstrap3')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    create_logger()
    admin.init_app(app)
    admin.add_view(ModelView(Teams, session))

    @app.route("/" + config.BOT_API_TOKEN, methods=['POST'])
    def get_message():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @app.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=f'{config.APP_HOST}/{config.BOT_API_TOKEN}')
        return 'Hook was set!', 200

    return app
