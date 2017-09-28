from bs4 import BeautifulSoup, element
from selenium import webdriver
import requests
import math

import time
import telebot
import config

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

class dota_parser():

    soup = ""

    def __init__(self):
        url = 'http://game-tournaments.com/dota-2/matches'
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def parse_future_matches(self):
        final_list = []
        tdes = self.soup.find('div', id="block_matches_current")
        for match in tdes.contents[1]:
            if type(match)!= element.NavigableString:
                local_list = []
                team1 = match.contents[3].contents[1].contents[1].contents[1].contents[1].contents[0]
                team2 =  match.contents[3].contents[1].contents[5].contents[3].contents[1].contents[0]
                local_list.append(str(team1))
                local_list.append(str(team2))
                tour_title = match.contents[7].contents[1].get('title')
                local_list.append(str(tour_title))
                if len(match.contents[5].contents[3].contents[1].contents) == 2:
                    local_list.append("Матч стартовал или вот-вот начнется!")
                else:
                    local_list.append("Матч состоится {}".format(match.contents[5].contents[3].contents[1].contents[0]))
                final_list.append(local_list)
        return final_list


    def parse_match(url):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        elem1 = driver.find_elements_by_class_name("t")
        elem1[1].click()




bot = telebot.TeleBot(config.token)
dp = dota_parser()
data_list = dp.parse_future_matches()
for math in data_list:
    bot.send_message(201501278, """
Dota2
*{}* -vs- *{}*
Турнир: *{}*.
 {}""".format(math[0],math[1],math[2],math[3]),parse_mode="Markdown")




