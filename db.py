import sqlite3
from random import sample


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`tg_id`) VALUES (?)",
                                       (tg_id,))

    def user_exists(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, tg_id, tg_name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `tg_name` = ? WHERE `tg_id` = ?",
                                       (tg_name, tg_id,))

    def get_nickname(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `tg_name` FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_quiz(self, quiz, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `quiz` = ? WHERE `tg_id` = ?",
                                       (quiz, tg_id,))

    def get_quiz(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `quiz` FROM `users` WHERE `tg_id` = ?",
                                         [tg_id]).fetchall()
            return result[0][0]

    def get_ques(self, num):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `quiz`").fetchall()
            return sample(result, num)

    def set_quiz_lvl(self, lvl, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `quiz_lvl` = ? WHERE `tg_id` = ?",
                                       (lvl, tg_id,))

    def get_quiz_lvl(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `quiz_lvl` FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                lvl = str(row[0])
            return lvl

    def set_num_que(self, num, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `num_que` = ? WHERE `tg_id` = ?",
                                       (str(num), tg_id,))

    def get_num_que(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `num_que` FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                num = int(row[0])
            return num

    def set_data_quest(self, data, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `que_user` (`tg_id`,`quest_data`) VALUES (?, ?)",
                                       (tg_id, str(data),))

    def get_data_quest(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `quest_data` FROM `que_user` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                data = str(row[0])
            return data

    def set_balance(self, balance, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `balance` = ? WHERE `tg_id` = ?",
                                       (balance, tg_id,)).fetchall()

    def get_balance(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `balance` FROM `users` WHERE `tg_id` = ?",
                                         (tg_id,)).fetchall()
            for row in result:
                balance = str(row[0])
            return balance