import SQLighter
import telebot
import dota_parser_lib
from config import token
from selenium import webdriver
from sys import platform


if __name__ == "__main__":
    if platform=="win32":
        driver = webdriver.PhantomJS('phantomjs.exe')
    else:
        try:
            driver = webdriver.PhantomJS()
        except Exception as e:
            print(e)
    driver.set_window_size(1080,1920)
    bot = telebot.TeleBot(token)
    sqler = SQLighter.DotaSqlClient()
    dota_info = dota_parser_lib.info_match(sqler, bot)
    dota_info.give_results_live(driver)
    dota_info.give_results_of_matches()
    dota_info.give_tour_pic(driver)
    #В конце удаляем завершенные матчи
    sqler.delete_finisher_matches()
    print('I try to tell all results!.')