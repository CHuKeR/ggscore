import SQLighter
from time import time
from selenium import webdriver
from time import sleep
import dota_parser_lib as dpl
import telebot
import config

from sys import platform

"""
if platform == "win32":
    driver = webdriver.PhantomJS('phantomjs.exe')
else:
    try:
        driver = webdriver.PhantomJS()
    except Exception as e:
        print(e)
#driver.set_window_size(1080, 1920)
"""
sqler = SQLighter.DotaSqlClient()
bot = telebot.TeleBot(config.token)
match_list = [
    "http://game-tournaments.com/dota-2/galaxy-battles-major/cis-2/double-dimension-vs-empire-58557"

]
match_q = ["DD","Empire","Galaxy Battles II: Emerging Worlds",None,"58557",None,"/dota-2/galaxy-battles-major/cis-2","/dota-2/galaxy-battles-major/cis-2/double-dimension-vs-empire-58557","1","0","None","0:0"]


def make_user_team_list(user_team_list):
    user_team_dict = {}
    for user in user_team_list:
        try:
            elem = user_team_dict[user[0]]
            user_team_dict[user[0]] = elem + user[1]
        except KeyError:
            user_team_dict[user[0]] = user[1]
    return user_team_dict

data_list = sqler.select_matches()
user_team_list = sqler.select_all_user_teams()
user_list = make_user_team_list(user_team_list)
for user in user_list.items():
    print(user[0])