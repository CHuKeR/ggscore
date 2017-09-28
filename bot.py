import config
import telebot
import os
import time
from random import shuffle
from SQLighter import SQLighter
import random
import utils

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["get_id"])
def get_user_id(message):
    bot.send_message(message.chat.id,message.chat.id)


@bot.message_handler(commands=["test"])
def find_file_ids(message):
    for file in os.listdir('music/'):
        if file.split(".")[-1] == "ogg":
            f = open("music/"+file,"rb")
            msg = bot.send_voice(message.chat.id,f,None,10)
            bot.send_message(message.chat.id,msg.voice.file_id,reply_to_message_id=msg.message_id)
        time.sleep(3)

@bot.message_handler(commands=['game'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__=="__main__":
    bot.polling(none_stop=True)