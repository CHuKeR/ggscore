import requests
from bs4 import BeautifulSoup, element
import SQLighter
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

file = open("teams1.txt")
for team in file:
    team = team.split(" ")
    for i in range(0,len(team)):
        team[i] = team[i].replace("\n","")
    sqler.up_team(team[0], " ".join(team[1:]))