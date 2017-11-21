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
sqler = SQLighter.DotaSqlClient()
callback_button_exit = types.InlineKeyboardButton(text="Закрыть настройки",
                                                     callback_data="close_settings")


@bot.message_handler(commands=["start"])
def add_user_id(message):
    try:
        sqler.add_user(message.chat.id)
    except Exception:
        pass
    # Под "остальным" понимаем состояние "0" - начало диалога
    bot.send_message(message.chat.id, "Добро пожаловать в IREU - бот, который сообщает вам о киберспортивных матчах."
                                      " На настоящий момент реализованы оповещения о матчах по Dota2. Каждый день в 0:00 по МСК вы получаете мачти на день. "
                                      "По заверщении серии вы получаете результат. Пока что это все, но у нас много планов на будущее. Если что - /help вам в помощь!"
                                      "Для настроек вводим /setting")

@bot.message_handler(commands=["setting"])
def add_user_id(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выбираем команды", callback_data="settigs_teams")
    callback_button1 = types.InlineKeyboardButton(text="Настройка оповещений", callback_data="setting_alerts")
    keyboard.row(callback_button,callback_button1)
    keyboard.add(callback_button_exit)
    bot.send_message(chat_id=message.chat.id, text="Выберите настройку:", reply_markup=keyboard)


@bot.message_handler(commands=["today"])
def add_user_id(message):
    sqler = SQLighter.DotaSqlClient()
    dota_info = dpl.info_match(sqler, bot)
    dota_info.give_today_matches(message.chat.id)

@bot.message_handler(commands=["help"])
def add_user_id(message):
    bot.send_message(message.chat.id,"Привет! Давай я тебе расскажу, какие команды тут есть:"
                                     "/start - если ты что-то забыл, я еще раз расскажу, кто я такой :)"
                                     "/today - выдает матчи на сегодня. Ты ничего не пропустишь!"
                                     "/setting - настройки."
                                     "+ тут есть секретная команда, если найдете - молодцы!"
                                     "По всем ошибкам и прочему писать: https://vk.com/prosto_chuker или @Chukerr в телеграмме.")

@bot.callback_query_handler(func=lambda call: True and call.data == "close_settings")
def back_to_start(call):
    if call.message:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: True and call.data == "setting")
def back_to_setting(call):
    if call.message:
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Выбираем команды", callback_data="settigs_teams")
        callback_button1 = types.InlineKeyboardButton(text="Настройка оповещений", callback_data="setting_alerts")
        keyboard.row(callback_button,callback_button1)
        keyboard.add(callback_button_exit)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                              text="Выберите настройку:", reply_markup=keyboard)


#Методы для настроек команд!

#Вывод регионов
@bot.callback_query_handler(func=lambda call: True and call.data== "settigs_teams")
def callback_inline2(call):
    if call.message:
        print(call.data)
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="СНГ", callback_data="team_CIS")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Европа", callback_data="team_Europe")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Китай", callback_data="team_China")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Северная Америка", callback_data="team_NA")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Южная Америка", callback_data="team_SA")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Юго-Восточная Азия", callback_data="team_Sea")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Сбросить все (выбираем все команды).", callback_data="team_reset")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Назад",callback_data="setting")
        keyboard.add(callback_button)
        keyboard.add(callback_button_exit)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text = "Выберите регион, с которого вы хотите добавить команды."
                                     " Изначально вы следите за всеми командами.", reply_markup=keyboard)

#Получить значение по ключу
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

#Вывыодим команды или сбрасываем до всех.
@bot.callback_query_handler(func=lambda call: True and call.data[:5]== "team_")
def callback_inline3(call):
    if call.message:
        print(call.data)
        keyboard = types.InlineKeyboardMarkup()
        if call.data[5:] != "reset":
            team_list = sqler.select_all_dota_teams(call.data[5:])
            numb = 0
            butt_list = []
            for team in team_list.values():
                callback_button = types.InlineKeyboardButton(text=team,
                                                             callback_data=str(get_key(team_list,team))+";")
                numb+=1
                butt_list.append(callback_button)
                if numb == 2:
                    keyboard.row(butt_list[0],butt_list[1])
                    numb=0
                    butt_list=[]
            if numb==1:
                keyboard.add(butt_list[0])
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="settigs_teams")
            keyboard.add(callback_button)
            mess = "Выбираем команды, которые хотим добавить."
        else:
            sqler.delete_user(call.message.chat.id)
            sqler.insert_user_pref(call.message.chat.id, "0;")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Все, следим за всеми!")
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="settigs_teams")
            keyboard.add(callback_button)
            mess = "Команды сброшены, что изволите делать дальше?"

        keyboard.add(callback_button_exit)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=mess, reply_markup=keyboard)

#Добавляем команду с проверкой
@bot.callback_query_handler(func=lambda call: True and call.data[-1:]== ";" and len(call.data)<4)
def callback_inline4(call):
    if call.message:
        user_pref = sqler.select_all_user_teams(call.message.chat.id)
        team_in = False
        if len(user_pref) == 1 and user_pref[0][1]== "0;":
            sqler.delete_user(call.message.chat.id)
        else:
            for team in user_pref:
                if call.data == team[1]:
                    team_in = True
        if team_in == False:
            sqler.insert_user_pref(call.message.chat.id, call.data)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Добавили!")
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы уже следите за этой командой!")


# Методы для настроек извещении

#Вывод списка команд юзера
@bot.callback_query_handler(func=lambda call: True and call.data == "setting_alerts")
def callback_inline5(call):
    user_pref = sqler.select_all_user_teams(user=call.message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    if len(user_pref) == 1 and user_pref[0][1]== "0;":
        mess = "Для начала выберите команды, чтобы настроить оповещения"
    else:
        team_list = sqler.select_all_dota_teams()
        numb = 0
        butt_list = []
        for team in user_pref:
            team_name = team_list[int(team[1][:-1])]
            numb+=1
            callback_button = types.InlineKeyboardButton(text=team_name,
                                                         callback_data="alerts_"+team[1])
            butt_list.append(callback_button)
            if numb == 2:
                keyboard.row(butt_list[0],butt_list[1])
                numb=0
                butt_list=[]
        if numb==1:
            keyboard.add(butt_list[0])
        mess = "Выберите команды для настроек изменений."
    callback_button = types.InlineKeyboardButton(text="Назад",callback_data="setting")
    keyboard.add(callback_button)
    keyboard.add(callback_button_exit)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=mess, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True and call.data[:7] == "alerts_")
def callback_inline6(call):
    user_pref = sqler.select_all_user_teams(user=call.message.chat.id, team=call.data[7:])
    keyboard = types.InlineKeyboardMarkup()
    for team in user_pref:
        team_list = sqler.select_all_dota_teams()
        mess = team_list[int(team[1][:-1])]
        if team[2]==0:
            add_match = "Серии"
        else:
            add_match = "Матча"
        after_match = types.InlineKeyboardButton(text="Результат отображется после "+ add_match,callback_data="change_mtc"+team[1])
        keyboard.add(after_match)
        if team[3] == 0:
            add_match = "не показывать."
        else:
            add_match = "показывать"
        after_tour = types.InlineKeyboardButton(text="Турнрирную сетку после матча "+ add_match,callback_data="change_trn"+team[1])
        keyboard.add(after_tour)
    callback_button = types.InlineKeyboardButton(text="Назад",callback_data="setting_alerts")
    keyboard.add(callback_button)
    keyboard.add(callback_button_exit)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Настройки для "+mess, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True and call.data[:7] == "change_")
def callback_inline7(call):
    if call.message:
        if call.data[7:10]=="mtc":
            sqler.update_user_pref(call.message.chat.id, call.data[10:], 0)
        else:
            sqler.update_user_pref(call.message.chat.id, call.data[10:], 1)
        user_pref = sqler.select_all_user_teams(user=call.message.chat.id, team=call.data[10:])
    keyboard = types.InlineKeyboardMarkup()
    for team in user_pref:
        team_list = sqler.select_all_dota_teams()
        mess = team_list[int(team[1][:-1])]
        if team[2]==0:
            add_match = "Серии"
        else:
            add_match = "Матча"
        after_match = types.InlineKeyboardButton(text="Результат отображется после "+ add_match,callback_data="change_mtc"+team[1])
        keyboard.add(after_match)
        if team[3] == 0:
            add_match = "не показывать."
        else:
            add_match = "показывать"
        after_tour = types.InlineKeyboardButton(text="Турнрирную сетку после матча "+ add_match,callback_data="change_trn"+team[1])
        keyboard.add(after_tour)
    callback_button = types.InlineKeyboardButton(text="Назад",callback_data="setting_alerts")
    keyboard.add(callback_button)
    keyboard.add(callback_button_exit)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Настройки для "+mess, reply_markup=keyboard)



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
