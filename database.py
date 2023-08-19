import sqlite3
import hashlib
import os



class EditTable:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()
    def create_table(self):
        '''Функция создания таблицы'''
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password_salt Varchar(128), password_hash Varchar(128), text TEXT)"
        )
        self.conn.commit()

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt, key

    def create_user_database(self, user):
        '''Функция создания пользователя'''
        self.create_table()

        query_check_login = "SELECT * FROM users WHERE login = ?"
        self.cursor.execute(query_check_login, (user[0],))
        existing_login = self.cursor.fetchone()

        query_check_email = "SELECT * FROM users WHERE email = ?"
        self.cursor.execute(query_check_email, (user[1],))
        existing_email = self.cursor.fetchone()

        if existing_email and existing_login:
            print('С этим логином и почтой уже существует учетная запись')
        elif existing_login:
            print('Этот логин уже занят')
        elif existing_email:
            print('Эта почта уже занята')
        else:
            salt, hashed_password = self.hash_password(user[2])
            self.cursor.execute("INSERT INTO users (login, email, password_salt, password_hash, text) VALUES "
                                "(?, ?, ?, ?, '')", (user[0], user[1], salt, hashed_password))
            self.conn.commit()
            print('Пользователь успешно создан!')


    def authenticate_user(self, login_or_email, password):
        '''Функция авторизации пользователя'''
        if not self.row_exists():
            return False

        query = "SELECT password_salt, password_hash FROM users WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (login_or_email, login_or_email))
        check = self.cursor.fetchone()

        if check:
            salt, saved_hash = check
            check_hash = self.hash_password(password, salt)[1]
            if saved_hash == check_hash:
                return True
        return None


    def delete_user_database(self, login_or_email, password):
        '''Функция удаления пользователя'''
        if not self.row_exists():
            return False

        query = "SELECT password_salt, password_hash FROM users WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (login_or_email, login_or_email))
        check = self.cursor.fetchone()

        if check:
            salt, saved_hash = check
            check_hash = self.hash_password(password, salt)[1]
            if saved_hash == check_hash:
                d_query = "DELETE FROM users WHERE (login = ? OR email = ?)"
                self.cursor.execute(d_query, (login_or_email, login_or_email))
                count = self.cursor.rowcount
                self.conn.commit()
                return count > 0
        return False

    def update_text(self, login, text):
        '''Функция обработки текста'''
        query = "UPDATE users SET text = ? WHERE login = ?"
        self.cursor.execute(query, (text, login))
        self.conn.commit()
        print('Текст успешно обновлен!')


    def delete_text(self, login):
        '''Функция обработки текста'''
        query_check = "SELECT text FROM users WHERE login = ?"
        self.cursor.execute(query_check, (login,))
        text_before_del = self.cursor.fetchone()

        query = "UPDATE users SET text = '' WHERE login = ?"
        self.cursor.execute(query, (login,))
        self.conn.commit()

        if text_before_del[0] == '':
            print('Запись еще не создана!')
        else:
            print('Запись удалена!')



    def show_text(self, login):
        '''Функция, которая принтует текст'''
        query = "SELECT text FROM users WHERE login = ?"
        self.cursor.execute(query, (login,))
        text = self.cursor.fetchone()

        if text[0] != '':
            print(text[0])
        else:
            print('Запись еще не создана!')

    def row_exists(self):
        '''Проверяет, есть ли строки в таблице'''
        try:
            self.cursor.execute("SELECT 1 FROM users LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False
