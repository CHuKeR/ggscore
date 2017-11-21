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
    "http://game-tournaments.com/dota-2/galaxy-battles-major/cis-2/double-dimension-vs-empire-58557"

]
match_q = ["DD","Empire","Galaxy Battles II: Emerging Worlds",None,"58557",None,"/dota-2/galaxy-battles-major/cis-2","/dota-2/galaxy-battles-major/cis-2/double-dimension-vs-empire-58557","1","0","None","0:0"]

tic = time()
url = "https://www.trackdota.com"
driver.get(url)
toc = time()
print("Open url: {}".format(toc - tic))
league_list = driver.find_elements_by_xpath("//*[@class='league_wrapper ng-scope']")
for match in league_list:
    match_list = match.find_elements_by_tag_name("a")
    for match in match_list:
        if match_q[0] in match.text or match_q[1] in match.text or \
                        match_q[0] in match.text or match_q[1] in match.text:
            print(match.get_attribute("href"))