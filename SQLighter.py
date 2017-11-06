import pymysql


class DotaSqlClient:

    def __init__(self):

        self.connection = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',
                                          port=3306,
                                          user='b1c0c21dcb6edc',
                                          passwd='3933112c',
                                          db='heroku_16092c835aedf9e',
                                          charset= "utf8")
        self.cursor = self.connection.cursor()

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
    def select_all_user_teams(self, user = None):
        with self.connection:
            if user == None:
                sql = "SELECT * FROM dota_db"
            else:
                sql = "SELECT * FROM dota_db where user_id = '{}'".format(user)
            self.cursor.execute(sql)
            team_list = self.cursor.fetchall()
            return team_list

    #Получаем список всех команд по Dota2 со всех регионов
    def select_all_dota_teams(self):
        with self.connection:
            sql = "SELECT team_name, id from dota_teams"
            self.cursor.execute(sql)
            dota_teams = self.cursor.fetchall()
            dota_teams_dict = dict((y, x) for x, y in dota_teams)
            return dota_teams_dict


    #Вставить будущий матч без результата (id, team1, team2, tournament, match_time)
    def insert_match(self,match):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO dota_matches(id, team1, team2, tournament, match_time) 
                VALUES('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE match_time='{}';"""
                                    .format(match[0],match[1],match[2],match[3],self.make_true_data(match[4]),self.make_true_data(match[4])))

    #Обновить результат по id матча
    def update_result(self,match):
        with self.connection:
            self.cursor.execute("""
                                UPDATE dota_matches SET result = '{}' WHERE id = '{}'"""
                                .format(match[5], match[0]))

    #Вставить команду в базу данных
    def insert_team(self,region,team_name):
        with self.connection:
            sql = 'insert into heroku_16092c835aedf9e.dota_teams (region,team_name) values("{}","{}")'.format(region,team_name)
            self.cursor.execute(sql)

    #Получаем список завершившихся матчей (т.е результат не пустой)
    def get_finished_matches(self):
        with self.connection:
            sql = "select * from dota_matches where `result` is not null"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    #Удаляем завершившихся матчах
    def delete_finisher_matches(self):
        with self.connection:
            sql = "delete from heroku_16092c835aedf9e.dota_matches where `result` is not null"
            self.cursor.execute(sql)

    #Получаем все матчи (в теории матчей с результатом быть не должно)
    def select_matches(self):
        with self.connection:
            sql = "select * from dota_matches"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def change_setting(self, chat_id, new_setting):
        with self.connection:
            self.cursor.execute(
                "REPLACE INTO dota_db (`user_id`, `news_flag`) VALUES('{}', '{}');".format(chat_id, new_setting))

    def add_user(self,user_id):
        with self.connection:
            sql = "insert into dota_db(user_id) values('{}')".format(user_id)
            self.cursor.execute(sql)
