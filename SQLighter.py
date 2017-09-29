import pymysql


class MySqlClient:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='heroku_16092c835aedf9e')
        self.cursor = self.connection.cursor()

    def change_setting(self,chat_id,new_setting):
        with self.connection:
            self.cursor.execute("REPLACE INTO dota_db (`user_id`, `news_flag`) VALUES('{}', '{}');".format(chat_id,new_setting))

    def select_all(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM dota_db").fetchall()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT IGNORE INTO `dota_db` SET `user_id` = '{}';".format(user_id))

    def close(self):
        self.connection.close()