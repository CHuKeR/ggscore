import config
import telebot
import utils
import SQLighter




bot = telebot.TeleBot(config.token)
settings = ["Оповещения о будущих матчах","Закрыть и сохранить настройки"]




@bot.message_handler(commands=["start"])
def add_user_id(message):
    sqlman = SQLighter.MySqlClient()
    sqlman.add_user(message.chat.id)
    bot.send_message(message.chat.id,"Hello!")


@bot.message_handler(commands=["setting"])
def get_user_id(message):
    utils.enable_settings_for_user(message.chat.id)
    markup = utils.generate_markup(settings)
    mess = utils.print_keyboard(settings)
    bot.send_message(message.chat.id,
    """
    Привет, давай настроим бота.
Выбери, что настраивать:\n""" + mess,reply_markup=markup)


@bot.message_handler(func=lambda message: utils.get_enable_setting(message.chat.id) != None, content_types=['text'])
def check_answer(message):
        if message.text == "Закрыть и сохранить настройки":
            utils.close_settings(message.chat.id)
        # Если пользователь в настройках
        settings_mode = utils.get_setting_mode(message.chat.id)
        if not settings_mode:
            # Проверяем, выбрано ли что-то
            if message.text == "1" or message.text == "Оповещения о будущих матчах":
                utils.enable_mode_for_user(message.chat.id,"10")
            else:
                bot.send_message(message.chat.id, 'Нет такого варианта =О!')
        elif settings_mode[0]=="1":
            if settings_mode[1]=="0":
                modes = ["Не присылать", "Только дневные (8:00-24:00)", "Только ночные (0:00-8:00)", "Присылать все!"]
                if message.text in modes:
                    utils.enable_mode_for_user(message.chat.id,"1{}".format(modes.index(message.text)+1))
                else:
                    utils.print_keyboard(modes)
            else:
                sql_client = SQLighter.MySqlClient
                sql_client.change_setting(message.chat.id,settings_mode[1])

@bot.message_handler(func=lambda message: utils.get_enable_setting(message.chat.id) == None, content_types=['text'])
def check_answer(message):
        bot.send_message(message.chat.id, 'Нет такого варианта =О! haha')


if __name__=="__main__":
    bot.polling(none_stop=True)


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

