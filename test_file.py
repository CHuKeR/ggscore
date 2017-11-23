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

id = 201501278
sqler = SQLighter.DotaSqlClient()
dota_info = dpl.info_match(sqler, bot)
dota_info.give_today_matches(id)
sqler.close()