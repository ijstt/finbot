import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`tg_id`) VALUES (?)", (tg_id,))

    def user_exists(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?", (tg_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, tg_id, tg_name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `tg_name` = ? WHERE `tg_id` = ?", (tg_name, tg_id,))

    def set_level(self, tg_id, level):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `level` =? WHERE `tg_id` = ?", (level, tg_id,))

    def get_level(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `level` FROM `users` WHERE `tg_id` = ?", (tg_id,)).fetchall()
            for row in result:
                level = row[0]
            return level
