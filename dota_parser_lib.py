import requests
from bs4 import BeautifulSoup, element
from selenium import webdriver
import datetime
import telebot
import config
import pytz

class dota_parser():

    soup = ""
    teams_with_id = {}
    sqler = ""

    def __init__(self, sqler):
        url = 'http://game-tournaments.com/dota-2/matches'
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, 'html.parser')
        self.sqler = sqler
        self.teams_with_id = sqler.select_all_dota_teams()

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

    def update_matches(self):
        #Парсим будущие матчи
        data_list = self.parse_future_matches()
        #Получаем список всех команд, которые парсим
        teams = self.teams_with_id.values()
        #Обновляем в БД будущие матчи (апдейты всего)
        for match in data_list:
            if (match[1] in teams or match[2] in teams) or (match[2] == "TBD" and match[1] == "TBD"):
                self.sqler.insert_match(match)
        #Парсим прошедшие матчи
        data_list = self.parse_prev_matches()
        #Обновляем их в БД
        for match in data_list:
           if  (match[1] in teams or match[2] in teams):
                self.sqler.update_result(match)

    def parse_match(self, url):
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        elem1 = driver.find_elements_by_class_name("t")
        elem1[1].click()


class info_match():

    sqler = ""


    def __init__(self,sqler, bot):
        self.sqler = sqler
        self.teams_with_id = sqler.select_all_dota_teams()
        self.bot = bot

    def make_user_team_list(self, user_prefer):
        if user_prefer == "0;":
            user_team_list = self.teams_with_id.values()
        # Иначе
        else:
            user_prefer = user_prefer.split(";")
            user_team_list = []
            for team in user_prefer[:-1]:
                user_team_list.append(self.teams_with_id[int(team)])
        return user_team_list

    def make_message_result(self,match):
        result = "*{} * -vs - * {} *\nTournament: *{} *\nResult: {}".format(match[0], match[1], match[2], match[3])
        return result

    def make_message_future(self,match):
        result = "*{} * -vs - * {} *\nTournament: *{} *\nTime: {}".format(match[0], match[1], match[2], match[5].split(" ")[2])
        return result

    def give_results_of_matches(self):
        #Получаем завершенные матчи
            data_list = self.sqler.get_finished_matches()
            #Список юзеров и их выбранных команд
            user_list = self.sqler.select_all_user_teams()
            for user in user_list:
                for match in data_list:
                    #Если 0 - то все матчи, иначе смотрим, что есть
                    user_team_list = self.make_user_team_list(user[1])
                    #Если эти матчи есть, то делаем результат, и выдаем это юзеру
                    if match[0] in user_team_list or match[1] in user_team_list:
                        mess = self.make_message_result(match)
                        # Может возникнуть ошибка, что нет юзера. Надо бы удалить/.
                        try:
                            self.bot.send_message(int(user[0]),mess, parse_mode="Markdown")
                        except telebot.apihelper.ApiException as e:
                            desc = eval(e.result.text.replace("false", "False"))
                            if desc== "Bad Request: chat not found":
                                self.sqler.delete_user(user)
            #В конце удаляем завершенные матчи
            self.sqler.delete_finisher_matches()

    def give_today_matches(self, asked_user = None):
        #asked_user вызывается, если пользователь запрашивает матчи с бота.
        #Обновляем день по МСК
        today = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow')).day
        month = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow')).month
        #Получаем матчи
        data_list = self.sqler.select_matches()
        if asked_user != None:
            user_list = self.sqler.select_all_user_teams(asked_user)
        else:
            user_list = self.sqler.select_all_user_teams()
        for user in user_list:
            self.bot.send_message(int(user[0]),"Матчи на {}.{}".format(today,month),parse_mode="Markdown")
            #Есть ли вообще матчи?
            yes_matches = False
            #Если все команды
            user_team_list = self.make_user_team_list(user[1])
            for match in data_list:
                if (match[0] in user_team_list or match[1] in user_team_list) and match[5][:len(str(today))] == str(today):
                    mess = self.make_message_future(match)
                    self.bot.send_message(int(user[0]),mess,parse_mode="Markdown")
                    yes_matches = True
            if yes_matches == False:
                self.bot.send_message(int(user[0]), "Нет мачтчей на сегодня!", parse_mode="Markdown")


