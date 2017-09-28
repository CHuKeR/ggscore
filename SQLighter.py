import sqlite3

class SQLighter:

    def __init__(self,database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM music").fetchall()

    def select_single(self, rownum):
        with self.connection:
            return  self.cursor.execute("SELECT * FROM music WHERE id = ?".format(rownum)).fetchall()[0]

    def count_rows(self):
        return len(self.select_all())

    def close(self):
        self.connection.close()