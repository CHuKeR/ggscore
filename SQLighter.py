import pymysql
from sys import platform

class DotaSqlClient:

    def __init__(self):
        if platform == "win32":
            self.connection = pymysql.connect(host='localhost',
                                              port=3306,
                                              user='root',
                                              passwd='123',
                                              db='heroku_16092c835aedf9e',
                                              charset="utf8")

        else:

            self.connection = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',
                                          port=3306,
                                          user='b1c0c21dcb6edc',
                                          passwd='3933112c',
                                          db='heroku_16092c835aedf9e',
                                          charset= "utf8")
        self.cursor = self.connection.cursor()



        #Методы, используемые для парсера сайта

    # Вставить будущий матч без результата (id, team1, team2, tournament, tour_link, match_link, live, *match_time)
    def insert_match(self, match):
            with self.connection:
                if len(match) ==  12:
                    sql = """
                    INSERT INTO dota_matches
                          (id, team1, team2, tournament, tour_link, match_link, live, match_time) 
                    VALUES('{}','{}', '{}',    '{}',            '{}',   '{}',     '{}',       '{}')
                     ON DUPLICATE KEY UPDATE match_time='{}',team1='{}',team2='{}', live = '{}';"""\
                        .format(match[0], match[1], match[2], match[3], match[4],match[5],match[6], self.make_true_data(match[7]),
                                            self.make_true_data(match[7]), match[1], match[2],match[6])
                else:
                    sql = """
                    INSERT INTO dota_matches(id, team1, team2, tournament, tour_link, match_link, live ) 
                    VALUES('{}','{}','{}','{}','{}','{}','{}')
                     ON DUPLICATE KEY UPDATE team1='{}',team2='{}', live = '{}';"""\
                        .format(match[0], match[1], match[2], match[3], match[4],match[5], match[6],
                                             match[1], match[2],match[6])
                self.cursor.execute(sql)

    # Обновить результат по id матча
    def update_result(self, match):
            with self.connection:
                self.cursor.execute("""
                                    UPDATE dota_matches SET result = '{}' WHERE id = '{}'"""
                                    .format(match[5], match[0]))

    # Сменит время с текста на цифры (а то БД жалуется)
    def make_true_data(self,old_time):
        old_time = old_time.split(",")
        timeq = old_time[1]
        new_data = old_time[0].split(" ")
        day = new_data[0]
        months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
                  "ноября",
                  "декабря"]
        new_mount = months.index(new_data[1]) + 1
        new_time = "{}.{}, {}".format(day, new_mount, timeq)
        return new_time

    # Получаем всех юзеров, которые зарегиститровались в приложении + команды, за которыми надо следить
    def select_all_user_teams(self, user = None,team = None, show_tour = None, show_match= None):
        with self.connection:
            sql = "SELECT * FROM dota_db"
            add_sql = []
            if user!= None:
                add_sql.append("user_id = '{}'".format(user))
            if show_match != None:
                add_sql.append("get_tour = '{}'".format(show_match))
            if team!= None:
                add_sql.append("teams_dota = '{}'".format(team))
            if show_tour!= None:
                add_sql.append("get_tour = '{}'".format(show_tour))
            if len(add_sql)!=0:
                final_sql = sql + " where " + " and ".join(add_sql)
            else:
                final_sql = sql
            self.cursor.execute(final_sql)
            team_list = self.cursor.fetchall()
            return team_list

    #Получаем все матчи (в теории матчей с результатом быть не должно)
    def select_matches(self):
        with self.connection:
            sql = "select * from dota_matches ORDER BY match_time"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    #Получаем список всех команд по Dota2 со всех регионов
    def select_all_dota_teams(self, region = None):
        with self.connection:
            if region==None:
                sql = "SELECT team_name, id from dota_teams"
            else:
                sql = "SELECT team_name, id from dota_teams where region = '{}'".format(region)
            self.cursor.execute(sql)
            dota_teams = self.cursor.fetchall()
            dota_teams_dict = dict((y, x) for x, y in dota_teams)
            return dota_teams_dict

    #Получаем все лайв матчи
    def select_live_matches(self):
        with self.connection:
            sql = "select * from dota_matches where live = 1"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    #Получаем список завершившихся матчей (т.е результат не пустой)
    def get_finished_matches(self):
        with self.connection:
            sql = "select * from dota_matches where `result` is not null ORDER BY match_time"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    #Удаляем завершившихся матчах
    def delete_finisher_matches(self):
        with self.connection:
            sql = "delete from heroku_16092c835aedf9e.dota_matches where `result` is not null"
            self.cursor.execute(sql)

    #Вставить предпочтения в командах
    def insert_user_pref(self, user, new_pref):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO dota_db (`user_id`, `teams_dota`) VALUES('{}', '{}');".format(user, new_pref))

    def update_user_pref(self, user, team, flag):
        with self.connection:
            if flag == 0:
                sql = "UPDATE dota_db SET after_match = not after_match  WHERE teams_dota = '{}' and user_id = '{}'"\
                    .format(team,user)
            else:
                sql = "UPDATE dota_db SET get_tour = not get_tour  WHERE teams_dota = '{}' and user_id='{}'"\
                    .format(team,user)
            self.cursor.execute(sql)



    #Удаляем юзера нахер
    def delete_user(self,user_id):
        with self.connection:
            sql = "delete from dota_db where user_id = '{}'".format(user_id)
            self.cursor.execute(sql)

    #Вставить команду в базу данных
    def insert_team(self,region,team_name):
        with self.connection:
            sql = 'insert into dota_teams (region,team_name) values("{}","{}")'.format(region,team_name)
            self.cursor.execute(sql)

    # Закончить матч (лайв = 0)
    def set_match_finisher(self, id):
        with self.connection:
            self.cursor.execute("UPDATE dota_matches SET live = 0 WHERE id = '{}'".format(id))

    # Увеличить число показанных матчей
    def inc_number_of_matches(self,id):
        with self.connection:
            self.cursor.execute("UPDATE dota_matches SET show_matches = show_matches+1  WHERE id = '{}'".format(id))

    # Добавить ссылку на трекдоту
    def set_td_link(self, id, href):
        with self.connection:
            self.cursor.execute("UPDATE dota_matches SET td_link = '{}'  WHERE id = '{}'".format(href,id))

    # Удалить ссылку на трекдоту
    def delete_td_link(self, id):
        with self.connection:
            self.cursor.execute("UPDATE dota_matches SET td_link = null  WHERE id = '{}'".format( id))

    # Обновить локальный результат
    def update_loc_res(self,id,res):
        with self.connection:
            self.cursor.execute("UPDATE dota_matches SET loc_res = '{}'  WHERE id = '{}'".format(res,id))



    def close(self):
        self.connection.close()


    def add_user(self,user_id):
        with self.connection:
            sql = "insert into dota_db(user_id) values('{}')".format(user_id)
            self.cursor.execute(sql)


