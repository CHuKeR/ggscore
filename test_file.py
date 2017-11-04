from time import time
from time import sleep
import SQLighter
import telebot
import config
from datetime import datetime

sum_time = 0
sqler = SQLighter.DotaSqlClient()
user_list = sqler.select_all_user_teams()
user_list[0]
user_list[1]
print(sum_time)
