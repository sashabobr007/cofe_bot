import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_drrink(self, user_id):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO drinks ('name') VALUES (?)", ( user_id,))


    def add_user(self, user_id, user):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO '{user}' ('user_id') VALUES (?)", ( user_id,))

    def drink_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM drinks WHERE name = ?", (user_id,)).fetchall()
            return bool(len(result))

    def user_exists(self, user_id, user):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM '{user}' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname, user):
        with self.connection:
            return self.cursor.execute(f"UPDATE '{user}' SET nickname = ? WHERE user_id = ?", (nickname, user_id,))

    def set_tg(self, user_id, nickname, user):
        with self.connection:
            return self.cursor.execute(f"UPDATE '{user}' SET tg_nick = ? WHERE user_id = ?", (nickname, user_id,))

    def set_zakaz(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET zakaz = ? WHERE user_id = ?", (cur, user_id,))

    def set_text_admin(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET text_admin = ? WHERE user_id = ?", (cur, user_id,))

    def set_sum(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET month_sum = ? WHERE user_id = ?", (cur, user_id,))

    def set_skidka(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET skidka = ? WHERE user_id = ?", (cur, user_id,))

    def set_skidka_cur(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET skidka_cur = ? WHERE user_id = ?", (cur, user_id,))


    def set_love_zakaz(self, user_id, cur):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET love_zakaz = ? WHERE user_id = ?", (cur, user_id,))

    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT nickname FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_skidka_cur(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT skidka_cur FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_skidka(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT skidka FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_love_zakaz(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT love_zakaz FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_text_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT text_admin FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_sum(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT month_sum FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_cur_pos(self, user_id, cur, user):
        with self.connection:
            return self.cursor.execute(f"UPDATE '{user}' SET cur_position = ? WHERE user_id = ?", (cur, user_id,))

    def get_tgnick(self, user_id, user):
        with self.connection:
            result = self.cursor.execute(f"SELECT tg_nick FROM '{user}' WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_cur_pos(self, user_id, user):
        with self.connection:
            result = self.cursor.execute(f"SELECT cur_position FROM '{user}' WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def user_del(self, user_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM drinks WHERE name = ?", (user_id,))

    def set_price(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(f"UPDATE drinks SET price = ? WHERE name = ?", (nickname, user_id,))

    def set_obem(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(f"UPDATE drinks SET obem = ? WHERE name = ?", (nickname, user_id,))

    def set_dobavki(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(f"UPDATE drinks SET dobavki = ? WHERE name = ?", (nickname, user_id,))

    def set_moloko(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(f"UPDATE drinks SET moloko = ? WHERE name = ?", (nickname, user_id,))

    def set_nal(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute(f"UPDATE drinks SET nalichie = ? WHERE name = ?", (nickname, user_id,))

    def get_all_drinks(self):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM drinks ").fetchall()
            return result

    def get_obem(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT obem FROM drinks WHERE name = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_moloko(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT moloko FROM drinks WHERE name = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_dobavki(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT dobavki FROM drinks WHERE name = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_zakaz(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT zakaz FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def get_price(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT price FROM drinks WHERE name = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup



