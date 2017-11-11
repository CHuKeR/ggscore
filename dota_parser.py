import dota_parser_lib
import SQLighter
import telebot
import config
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

sched = BlockingScheduler()

"""
@sched.scheduled_job('interval', minutes=15 ,timezone = pytz.timezone("Europe/Moscow"))
def timed_job():
    sqler = SQLighter.DotaSqlClient()
    dp = dota_parser_lib.dota_parser(sqler)
    dp.update_matches()
    sqler.close()
    print('Update DB')
"""

@sched.scheduled_job('interval', minutes=60, timezone = pytz.timezone("Europe/Moscow"))
def timed_job():
    sqler = SQLighter.DotaSqlClient()
    bot = telebot.TeleBot(config.token)
    dota_info = dota_parser_lib.info_match(sqler, bot)
    dota_info.give_results_of_matches()
    sqler.close()
    print('I try to tell all results!.')

@sched.scheduled_job('cron',  hour=0, timezone = pytz.timezone("Europe/Moscow"))
def scheduled_job():
    sqler = SQLighter.DotaSqlClient()
    bot = telebot.TeleBot(config.token)
    dota_info = dota_parser_lib.info_match(sqler, bot)
    dota_info.give_today_matches()
    sqler.close()
    print('I try to tell all matches!')

sched.start()


