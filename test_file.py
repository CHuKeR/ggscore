import SQLighter
import telebot
import config

bot = telebot.TeleBot(config.token)
sqler = SQLighter.DotaSqlClient()

user_list = sqler.select_all_user_teams()
for user in user_list:
    try:
        bot.send_message(int(user[0]), "lolkek", parse_mode="Markdown")
    except telebot.apihelper.ApiException as e:
        desc = eval(e.text.replace("false", "False"))
        print()
        if desc == "Bad Request: chat not found":
            sqler.delete_user(user)