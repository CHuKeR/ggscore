import dota_parser_lib
import datetime
import SQLighter
from time import sleep, time

if __name__ == "__main__":
    counter = 0
    today = datetime.datetime.today().day
    while True:
        counter+=1
        tic = time()
        sqler = SQLighter.DotaSqlClient()
        teams_with_id = sqler.select_all_dota_teams()
        dp = dota_parser_lib.dota_parser(sqler)
        dp.update_matches()
        #Каждое 4 обновление скрипта отдаем результаты матчей юзерам
        if counter%4==0:
            dota_info = dota_parser_lib.info_match(sqler)
            dota_info.give_results_of_matches()
            counter = 0
        #Новый день - пишем матчи на сегодня
        if today != datetime.datetime.today().day:
            dota_info = dota_parser_lib.info_match(sqler)
            dota_info.give_today_matches(sqler)
        toc = time()
        print(toc - tic)
        sleep(2)
