import config
import telebot
import utils




bot = telebot.TeleBot(config.token)
settings = ["Оповещения о будущих матчах"]

@bot.message_handler(commands=["setting"])
def get_user_id(message):
    utils.enable_settings_for_user(message.chat.id)
    mess = ""
    num = 1
    markup = utils.generate_markup(settings)
    for item in settings:
        mess+="{}. {}\n".format(num,item)
    bot.send_message(message.chat.id,
    """
    Привет, давай настроим бота.
    Выбери, что настраивать:\n""" + mess,reply_markup=markup)



@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_user_answer(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Если хотите настроек, выберите команду /setting (пока тут больше ничего нет)')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == "1" or settings.index(message.text) == 0:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Нет такого варианта =О!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища
        utils.delete_user_settings(message.chat.id)

@bot.message_handler(commands=["322"])
def get_user_id(message):
    bot.send_message(message.chat.id,
"""
Первое правило ставок - не ставить на Na'Vi.
Второе правило ставок - не ставь против Na'Vi.
"""
)

@bot.message_handler(commands=["get_id"])
def get_user_id(message):
    bot.send_message(message.chat.id,message.chat.id)

if __name__=="__main__":
    bot.polling(none_stop=True)