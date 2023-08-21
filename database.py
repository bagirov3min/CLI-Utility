import sqlite3
import hashlib
import os



class EditTable:
    '''Работаем с базой данных'''
    def __init__(self):
        '''Указываем параметры работы для с базой данных'''
        self.conn = sqlite3.connect("users.sqlite")  # Создаем коннектор к базе
        self.cursor = self.conn.cursor()  # Создаем курсор
    def create_table(self):
        '''Функция создания таблицы с предопределенными столбцами'''
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password_salt Varchar(128), password_hash Varchar(128), text TEXT)"
        )
        self.conn.commit()

    def hash_password(self, password: str, salt=None):
        '''Хешируем пароль'''
        if salt is None:
            salt = os.urandom(16)  # Генерируем случайную соль
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        # Хешируем пароль с использованием соли
        return salt, key

    def create_user_database(self, user: tuple):
        '''Функция создания пользователя, принимает список'''
        self.create_table()  # Создаем таблицу, если она не была еще создана

        # Делаем запрос к таблице, проверяем есть ли такой логин
        query_check_login = "SELECT * FROM users WHERE login = ?"
        self.cursor.execute(query_check_login, (user[0],))
        existing_login = self.cursor.fetchone()

        # Делаем запрос к таблице, проверяем есть ли такой email
        query_check_email = "SELECT * FROM users WHERE email = ?"
        self.cursor.execute(query_check_email, (user[1],))
        existing_email = self.cursor.fetchone()

        if existing_email and existing_login:
            print('С этим логином и почтой уже существует учетная запись')
        elif existing_login:
            print('Этот логин уже занят')
        elif existing_email:
            print('Эта почта уже занята')
        # Если пользователя еще не существует, то мы передаем на хеширование пароль, а после добавляем в базу
        # логин, email, соль и хешированный пароль
        else:
            salt, hashed_password = self.hash_password(user[2])
            self.cursor.execute("INSERT INTO users (login, email, password_salt, password_hash, text) VALUES "
                                "(?, ?, ?, ?, '')", (user[0], user[1], salt, hashed_password))
            self.conn.commit()
            print('Пользователь успешно создан!')


    def authenticate_user(self, user: tuple):
        '''Функция авторизации пользователя'''
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False

        # Передаем в таблицу введенные данные от пользователя, логин или email
        query = "SELECT password_salt, password_hash FROM users WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (user[0], user[0]))
        check = self.cursor.fetchone()

        # Проверяем, если запрос check имеет данные, то проводим авторизацию и возвращаем True
        # Если в запросе в таблицу пустое значение, то возвращаем его, принимающая функция его обработает
        # Для безопасной работы мы хешируем вновь полученный от пользователя пароли и сравниваем его с
        # сохраненным захешируеным паролем
        if check:
            salt, saved_hash = check
            check_hash = self.hash_password(user[1], salt)[1]
            if saved_hash == check_hash:
                return True
        return None


    def delete_user_database(self, user: tuple):
        '''Функция удаления пользователя'''
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False

        # Передаем в таблицу введенные данные от пользователя, логин или email
        query = "SELECT password_salt, password_hash FROM users WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (user[0], user[0]))
        check = self.cursor.fetchone()

        # Проверяем, если запрос check не имеет данных, то возвращаем False
        # Если данные по веденному логину или email есть в таблице, то начинаем работать с полученными данными
        # Для безопасной работы мы хешируем вновь полученный от пользователя пароли и сравниваем его с
        # сохраненным захешируеным паролем. Если пароли совпадают, делаем запрос на удаление строки в базу
        if check:
            salt, saved_hash = check
            check_hash = self.hash_password(user[1], salt)[1]
            if saved_hash == check_hash:
                d_query = "DELETE FROM users WHERE (login = ? OR email = ?)"
                self.cursor.execute(d_query, (user[0], user[0]))
                count = self.cursor.rowcount
                self.conn.commit()
                return count > 0
        return False

    def update_text(self, login: str, text: str):
        '''Функция обновления текста'''
        query = "UPDATE users SET text = ? WHERE login = ?"  # Ищем столбец text в строке где есть введенный login
        self.cursor.execute(query, (text, login))  # Передаем данные введенные пользователем
        self.conn.commit()
        print('Текст успешно обновлен!')


    def delete_text(self, login: str):
        '''Функция удаления текста'''
        query_check = "SELECT text FROM users WHERE login = ?"  # Ищем столбец text в строке где есть введенный login
        self.cursor.execute(query_check, (login,))
        text_before_del = self.cursor.fetchone()  # Сохраняем текст, который был в столбце

        # Ищем столбец text в строке где есть введенный login и обновляем его пустой строкой ""
        query = "UPDATE users SET text = '' WHERE login = ?"
        self.cursor.execute(query, (login,))
        self.conn.commit()

        # Проверяем, существовала ли вообще строка до этого запроса и возвращаем нужный ответ
        if text_before_del[0] == '':
            print('Запись еще не создана!')
        else:
            print('Запись удалена!')



    def show_text(self, login: str):
        '''Функция вывода текста на экран'''
        query = "SELECT text FROM users WHERE login = ?"  # Ищем столбец text в строке где есть введенный login
        self.cursor.execute(query, (login,))
        text = self.cursor.fetchone()

        # Проверяем, существовала ли вообще строка до этого запроса и возвращаем нужный ответ
        if text[0] != '':
            print(text[0])
        else:
            print('Запись еще не создана!')

    def row_exists(self):
        '''Проверяет, есть ли строки в таблице и возвращает нужный ответ'''
        try:
            self.cursor.execute("SELECT 1 FROM users LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False

