import requests
from bs4 import BeautifulSoup, element
import datetime
import telebot
import pytz
from time import time, sleep
from PIL import Image
from io import BytesIO

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
                tour_title = match.contents[7].contents[1].attrs['title']
                local_list.append(str(tour_title))
                tour_link = match.contents[7].contents[1].attrs['href']
                local_list.append(tour_link)
                match_link = match.contents[3].contents[1].attrs["href"]
                local_list.append(match_link)
                if "class" not in match.attrs:
                    local_list.append(0)
                    local_list.append(match.contents[5].contents[3].contents[1].contents[0])
                    final_list.append(local_list)
                else:
                    local_list.append(1)
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

    def make_message_live(self,match):
        if len(match)==5:
            result = "{} Победили! \n {}  - {} -  {} \n".format(match[3],match[0],match[4], match[1])
        else:
            result = "К сожалению не получилось получить счёт серии. \n" \
                     "{}  - vs -  {} ".format(match[0],match[1])
        return result

    def give_results_of_matches(self):
        #Получаем завершенные матчи
            data_list = self.sqler.get_finished_matches()
            #Список юзеров и их выбранных команд
            user_list = self.sqler.select_all_user_teams(show_match=0)
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

    def give_tour_pic(self,driver):
        #Получаем завершенные матчи
            data_list = self.sqler.get_finished_matches()
            #Список юзеров и их выбранных команд
            user_list = self.sqler.select_all_user_teams(show_tour=1)
            for user in user_list:
                for match in data_list:
                    #Если 0 - то все матчи, иначе смотрим, что есть
                    user_team_list = self.make_user_team_list(user[1])
                    #Если эти матчи есть, то делаем результат, и выдаем это юзеру
                    if match[0] in user_team_list or match[1] in user_team_list:
                        mess = self.make_message_result(match)
                        # Может возникнуть ошибка, что нет юзера. Надо бы удалить/.
                        try:
                            pic = self.get_tournament_res(match[6],driver)
                            mess = "Турнирная таблица "+ match[2]
                        except Exception:
                            print("Ошибка с картинкой турнира!")
                        try:
                            self.bot.send_photo(int(user[0]),pic,caption=mess)
                        except telebot.apihelper.ApiException as e:
                            desc = eval(e.result.text.replace("false", "False"))
                            if desc== "Bad Request: chat not found":
                                self.sqler.delete_user(user)

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

    def give_results_live(self, driver):
        res_list = self.get_results_of_live(driver)
        user_list = self.sqler.select_all_user_teams(show_match=1)
        for user in user_list:
            for match in res_list:
                user_team_list = self.make_user_team_list(user[1])
                #Если эти матчи есть, то делаем результат, и выдаем это юзеру
                if match[0] in user_team_list or match[1] in user_team_list:
                    mess = self.make_message_live(match)
                    # Может возникнуть ошибка, что нет юзера. Надо бы удалить/.
                    try:
                        self.bot.send_photo(int(user[0]),photo=match[2],caption=mess)
                    except telebot.apihelper.ApiException as e:
                        desc = eval(e.result.text.replace("false", "False"))
                        print("Нет чата")
                        if desc== "Bad Request: chat not found":
                            self.sqler.delete_user(user)

    def get_results_of_live(self,driver):
        match_list = self.sqler.select_live_matches()
        final_list = []
        for match in match_list:
            if match[10] == None or match[10]=="None":
                href = self.find_track_dota_link(match[0],match[1],driver)
                self.sqler.set_td_link(match[4],href)
            picture = self.parse_live_match(driver,match)
            if picture!=None:
                if match[10]!="None":
                    winner = self.get_winner(driver,match[10])
                    new_res = self.update_loc_res(winner,match[11],match[0],match[1])
                    self.sqler.update_loc_res(match[4],new_res)
                    final_list.append([match[0],match[1],picture,winner,new_res])
                else:
                    self.sqler.delete_td_link(match[4])
                    final_list.append([match[0],match[1],picture])

        return final_list

    def find_track_dota_link(self, team1, team2, driver):
        tic = time()
        url = "https://www.trackdota.com"
        driver.get(url)
        toc = time()
        print("Open url: {}".format(toc - tic))
        league_list = driver.find_elements_by_xpath("//*[@class='league_wrapper ng-scope']")
        for match in league_list:
            match_list = match.find_elements_by_tag_name("a")
            for match in match_list:
                if team1 in match.text or team2 in match.text:
                    return match.get_attribute("href")

    def parse_live_match(self, driver,match):
        driver.get("http://game-tournaments.com"+match[7])
        games = driver.find_elements_by_class_name("t")
        picture = None
        try:
            games[match[9]].click()
            sleep(1)
            if "LIVE" not in games[match[9]].text:
                try:
                    tic = time()
                    picture = driver.find_element_by_partial_link_text("результаты").get_attribute("href")
                    toc = time()
                    print("get pc {}".format(toc-tic))
                except Exception as e:
                    print(e)
                    if not driver.find_elements_by_partial_link_text("LIVE"):
                        self.sqler.set_match_finisher(match[4])
                    else:
                        print("LIVE_PARTY")
                        self.sqler.inc_number_of_matches(match[4])
                else: self.sqler.inc_number_of_matches(match[4])
        except IndexError:
            print("Матчи закончились")
            self.sqler.set_match_finisher(match[4])
        return picture

    def get_winner(self,driver,url):
        driver.get(url)
        winner = driver.find_elements_by_class_name("column")[2].text.split("\n")[2]
        return winner

    def update_loc_res(self,winner,loc_res, team1, team2):
        loc_res = loc_res.split(":")
        print(winner,loc_res,team1,team2)
        if winner.lower() in team1.lower():
            new_res = str(int(loc_res[0])+1)+":"+loc_res[1]
        elif winner.lower() in team2.lower():
            new_res = loc_res[0]+":"+str(int(loc_res[1])+1)
        else: new_res = "TROUBE"
        return new_res

    def get_tournament_res(self, url, driver):
        driver.get("http://game-tournaments.com"+url)
        element =driver.find_elements_by_class_name("col-sm-12")[0]
        location = element.location
        size = element.size
        im = Image.open(BytesIO(element.screenshot_as_png))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom)) # defines crop points
        imgByteArr = BytesIO()
        im.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr