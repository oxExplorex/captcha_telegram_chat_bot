import sqlite3

class SQL:
    def __init__(self):
        self.connection = sqlite3.connect("database/db.db")
        self.cursor = self.connection.cursor()

    def create_table(self, user_id):
        try:
            with self.connection:
                self.cursor.execute(f'CREATE TABLE [{user_id}_chat] (user_id INTEGER, message_id INTEGER)')
                self.cursor.execute(f'CREATE TABLE [{user_id}_verify] (user_id INTEGER, verify INTEGER)')
            return True
        except:
            return False

    def add_new_message(self, chat_id, user_id, message_id):
        with self.connection:
            self.cursor.execute(f"INSERT INTO `{str(chat_id) + '_chat'}` (`user_id`, `message_id`) VALUES (?,?)", (user_id, message_id, ))

    def add_verify(self, chat_id, user_id):
        with self.connection:
            return self.cursor.execute(f"UPDATE `{str(chat_id) + '_verify'}` SET `verify` = ? WHERE `user_id` = ?", (1, user_id,))

    def check_user(self, chat_id, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{str(chat_id) + '_verify'}` WHERE user_id = ?", (user_id,)).fetchone()

    def add_new_user(self, chat_id, user_id):
        with self.connection:
            self.cursor.execute(f"INSERT INTO `{str(chat_id) + '_verify'}` (`user_id`, `verify`) VALUES (?,?)", (user_id, 0, ))

    def get_count_messages(self, chat_id, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{str(chat_id) + '_chat'}` WHERE user_id = ?", (user_id,)).fetchall()


