import SQLighter
import telebot
import dota_parser_lib
from config import token

if __name__ == "__main__":
    sqler = SQLighter.DotaSqlClient()
    bot = telebot.TeleBot(token)
    dota_info = dota_parser_lib.info_match(sqler, bot)
    dota_info.give_today_matches()
    sqler.close()
    print('I try to tell all matches!')
