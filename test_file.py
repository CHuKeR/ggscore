import SQLighter
from time import time
from selenium import webdriver
import telebot
import config
from urllib import request
from time import sleep
import dota_parser_lib as dpl

sqler = SQLighter.DotaSqlClient()
bot = telebot.TeleBot(config.token)
dota_info = dpl.info_match(sqler, bot)
dota_info.give_today_matches(201501278)


