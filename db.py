import sqlite3
from datetime import datetime, timezone


# to read: migrations, db models and ORM, sql injections

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """get user id by he's telegram id"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, name):
        print(f"user id = {user_id}")
        print(f"name = {name}")
        self.cursor.execute("INSERT INTO 'users' ('user_id', 'name') VALUES (?, ?)", (user_id, name))
        return self.conn.commit()

    def rm_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, alarm_time):
        self.cursor.execute("INSERT INTO 'records' ('users_id', 'alarm_time') VALUES (?, ?)",
                            (self.get_user_id(user_id),
                             datetime.now(timezone.utc)))

    def get_records(self, user_id):
        result = ("SELECT * FROM 'records' WHERE 'user_id' = ?", self.get_user_id(user_id))
        return result.fetchall()

    def get_name(self, user_id):
        result = self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
        item = result.fetchone()
        if item is None:
            return None
        else:
            return item[0]

    def close(self):
        self.conn.close()
