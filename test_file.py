import SQLighter
from time import time
from selenium import webdriver
import telebot
import config
from urllib import request
from time import sleep


sqler = SQLighter.DotaSqlClient()
tic = time()
driver = webdriver.PhantomJS("phantomjs.exe")
toc = time()
print("Открыть браузер " + str(toc-tic))
url = "http://game-tournaments.com/dota-2/captains-draft-4/cis/vega-vs-spirit-57398"
tic = time()
driver.get(url)
toc = time()
print("Открыть ссылку " + str(toc-tic))
tic = time()
elem1 = driver.find_elements_by_class_name("t")
toc = time()
print("Открыть найти вкладку " + str(toc-tic))
tic = time()
elem1[1].click()
toc = time()
print("Click: " + str(toc-tic))
sleep(5)
tic = time()
url_image = driver.find_elements_by_partial_link_text('Показать результаты игры')[0].get_attribute("href")
toc = time()
print("find href " + str(toc-tic))
#bot = telebot.TeleBot(config.token)
#bot.send_photo(201501278,photo=url_image)
driver.close()


