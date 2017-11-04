from bs4 import BeautifulSoup, element
from selenium import webdriver
import requests
from time import time
from time import  sleep
import SQLighter
import datetime
import telebot
import config

class dota_parser():

    soup = ""
    first_future_match = ""
    first_past_match = ""

    def __init__(self):
        url = 'http://game-tournaments.com/dota-2/matches'
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def parse_future_matches(self):
        final_list = []
        table_match = self.soup.find('div', {"id" : "block_matches_current"})
        for match in table_match.contents[1].contents:
            if type(match)!= element.NavigableString:
                local_list = []
                id = match.attrs["rel"]
                local_list.append(id)
                team1 = match.contents[3].contents[1].contents[1].contents[1].contents[1].contents[0]
                team2 =  match.contents[3].contents[1].contents[5].contents[3].contents[1].contents[0]
                local_list.append(str(team1))
                local_list.append(str(team2))
                tour_title = match.contents[7].contents[1].get('title')
                local_list.append(str(tour_title))
                if len(match.contents[5].contents[3].contents[1].contents) != 2:
                    local_list.append(match.contents[5].contents[3].contents[1].contents[0])
                    final_list.append(local_list)
        return final_list

    def parse_prev_matches(self):
        final_list = []
        table_match = self.soup.find('div', {"id": "block_matches_past"})
        for match in table_match.contents[1].contents:
            if type(match) != element.NavigableString:
                local_list = []
                id = match.attrs["rel"]
                local_list.append(id)
                team1 = match.contents[3].contents[1].contents[1].contents[1].contents[1].contents[0]
                result = match.contents[3].contents[1].contents[3].contents[3].contents[1].attrs["data-score"]
                team2 = match.contents[3].contents[1].contents[5].contents[3].contents[1].contents[0]
                local_list.append(str(team1))
                local_list.append(str(team2))
                tour_title = match.contents[7].contents[1].get('title')
                local_list.append(str(tour_title))
                if len(match.contents[5].contents[3].contents[1].contents) != 2:
                    local_list.append(match.contents[5].contents[3].contents[1].contents[0])
                    local_list.append(result)
                    final_list.append(local_list)
        return final_list

    def make_message_result(self,match):
        result = "Dota2\n*{} * -vs - * {} *\nTournament: *{} *\nResult: {}".format(match[0], match[1], match[2], match[3])
        return result

    def make_message_future(self,match):
        result = "Dota2\n*{} * -vs - * {} *\nTournament: *{} *\nTime: {}".format(match[0], match[1], match[2], match[5])
        return result


    def parse_match(url):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        elem1 = driver.find_elements_by_class_name("t")
        elem1[1].click()

if __name__ == "__main__":
    counter = 0
    today = datetime.datetime.today().day
    while True:
        counter+=1
        tic = time()
        dp = dota_parser()
        sqler = SQLighter.DotaSqlClient()

        #Парсим будущие матчи
        data_list = dp.parse_future_matches()
        #Получаем список всех команд, которые парсим
        teams_with_id = sqler.select_all_dota_teams()
        teams = teams_with_id.values()
        #Обновляем в БД будущие матчи (апдейты всего)
        for match in data_list:
            if (match[1] in teams or match[2] in teams) or (match[2] == "TBD" and match[1] == "TBD"):
                sqler.insert_match(match)

        #Парсим прошедшие матчи
        data_list = dp.parse_prev_matches()
        #Обновляем их в БД
        for match in data_list:
           if  (match[1] in teams or match[2] in teams):
                sqler.update_result(match)

        #Каждое 4 обновление скрипта отдаем результаты матчей юзерам
        if counter%4==0:
            #Получаем завершенные матчи
            data_list = sqler.get_finished_matches()
            #Инит бота
            bot = telebot.TeleBot(config.token)
            #Список юзеров и команд
            user_list = sqler.select_all_user_teams()
            for user in user_list:
                for match in data_list:
                    #Если 0 - то все матчи, иначе смотрим, что есть
                    if user[1]=="0;":
                        user_team_list = teams
                    else:
                        #Получаем список матчей и загружаем его в список
                        user_prefer = user[1].split(";")
                        user_team_list = []
                        for team in user_prefer:
                            user_team_list.append(teams_with_id[team])
                    #Если эти матчи есть, то делаем результат, и выдаем это юзеру
                    if match[0] in user_team_list or match[1] in user_team_list:
                        mess = dp.make_message_result(match)
                        bot.send_message(int(user[0]),mess, parse_mode="Markdown")
            sqler.delete_finisher_matches()
            counter = 0
        #Новый день - пишем матчи на сегодня
        if today != datetime.datetime.today().day:
            # Инит бота
            bot = telebot.TeleBot(config.token)
            #Обновляем день
            today = datetime.datetime.today().day
            #Получаем матчи
            data_list = sqler.select_matches()
            user_list = sqler.select_all_user_teams()
            for user in user_list:
                for match in data_list:
                    if user[1]=="0;":
                        user_team_list = teams
                    else:
                        user_prefer = user[1].split(";")
                        user_team_list = []
                        for team in user_prefer:
                            user_team_list.append(teams_with_id[team])
                    if (match[0] in user_team_list or match[1] in user_team_list) and match[5][:len(str(today))] == str(today):
                        mess = dp.make_message_future(match)
                        bot.send_message(int(user[0]),mess,parse_mode="Markdown")
        toc = time()
        print(toc - tic)
        sleep(900)
