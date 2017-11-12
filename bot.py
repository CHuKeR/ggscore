import config
import telebot
import SQLighter
import dota_parser_lib as dpl
import os
from flask import Flask, request
from telebot import types


bot = telebot.TeleBot(config.token)
settings = ["Оповещения о будущих матчах","Закрыть и сохранить настройки"]
server = Flask(__name__)


@bot.message_handler(commands=["start"])
def add_user_id(message):
    sqler = SQLighter.DotaSqlClient()
    try:
        sqler.add_user(message.chat.id)
    except Exception:
        pass

    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Получить матчи на сегодня!", callback_data="today")
    keyboard.add(callback_button)
    # Под "остальным" понимаем состояние "0" - начало диалога
    bot.send_message(message.chat.id,"Добро пожаловать в IREU - бот, который сообщает вам о киберспортивных матчах."
                                     " На настоящий момент реализованы оповещения о матчах по Dota2. Каждый день в 0:00 по МСК вы получаете мачти на день. "
                                     "По заверщении серии вы получаете результат. Пока что это все, но у нас много планов на будущее. Если что - /help вам в помощь! :),",reply_markup=keyboard)



@bot.message_handler(commands=["help"])
def add_user_id(message):
    bot.send_message(message.chat.id,"Привет! Давай я тебе расскажу, какие команды тут есть:"
                                     "/start - если ты что-то забыл, я еще раз расскажу, кто я такой :)"
                                     "/today - выдает матчи на сегодня. Ты ничего не пропустишь!"
                                     "+ тут есть секретная команда, если найдете - молодцы!"
                                     "По всем ошибкам и прочему писать: https://vk.com/prosto_chuker или @Chukerr в телеграмме.")



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "today":
            sqler = SQLighter.DotaSqlClient()
            dota_info = dpl.info_match(sqler, bot)
            dota_info.give_today_matches(call.message.chat.id)


@bot.message_handler(commands=["today"])
def add_user_id(message):
    sqler = SQLighter.DotaSqlClient()
    dota_info = dpl.info_match(sqler, bot)
    dota_info.give_today_matches(message.chat.id)


@bot.message_handler(commands=["322"])
def get_user_id(message):
    bot.send_message(message.chat.id,
"""
Первое правило ставок - не ставить на Na'Vi.
Второе правило ставок - не ставь против Na'Vi.
"""
)


@server.route("/"+config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://ireu.herokuapp.com/"+config.token)
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
