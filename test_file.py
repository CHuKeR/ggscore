import SQLighter
from time import time
from selenium import webdriver
from time import sleep

from sys import platform

if platform == "win32":
    driver = webdriver.PhantomJS('phantomjs.exe')
else:
    try:
        driver = webdriver.PhantomJS()
    except Exception as e:
        print(e)
driver.set_window_size(1080, 1920)
sqler = SQLighter.DotaSqlClient()

match_list = [
    "http://game-tournaments.com/dota-2/galaxy-battles-major/sea-1/clutch-gamers-vs-execration-58507",
    "http://game-tournaments.com/dota-2/adrenaline-cyber-league-2017/playoff/navi-vs-mouz-58495",
    "http://game-tournaments.com/dota-2/prodota-cup-china-1/playoff/sun-gaming-vs-keen-gaming-58005",
    "http://game-tournaments.com/dota-2/aef-dota-2-league-season-3/division-3/nah-bro-vs-tempest-au-58739",
    "http://game-tournaments.com/dota-2/aef-dota-2-league-season-3/division-2/sweet-original-name-vs-le-voyage-58738",
    "http://game-tournaments.com/dota-2/galaxy-battles-major/south-america-2/sacred-vs-sage-network-57880",
    "http://game-tournaments.com/dota-2/midas-mode/group/vgj-storm-vs-evil-geniuses-56204"

]
for match in match_list:
    driver.get(match)
    games = driver.find_elements_by_class_name("t")
    picture = None
    try:
        games[0].click()
        sleep(1)
        if "LIVE" not in games[0].text:
            try:
                tic = time()
                picture = driver.find_element_by_partial_link_text("результаты").get_attribute("href")
                print(picture)
                toc = time()
                print("get pc {}".format(toc-tic))
            except Exception as e:
                print(e)
                if not driver.find_elements_by_partial_link_text("LIVE"):
                    print("match finisg")
                else:
                    print("LIVE_PARTY")

            else: print("Матч +1")
    except IndexError:
        print("Матчи закончились")
