import sqlite3
import hashlib
import os


def hash_password(password: str, salt: bytes = None):
    """Хэшируем пароль"""
    if salt is None:
        salt = os.urandom(16)  # Генерируем случайную соль
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Хэшируем пароль с использованием соли
    return salt, key


class Database:
    """Работаем с базой данных"""
    USERS_TABLE_NAME = "users_table"
    TEXT_TABLE_NAME = "text_table"

    def __init__(self, table_name: str):
        """Указываем параметры работы для с базой данных"""
        self.conn = sqlite3.connect("users.sqlite")  # Создаем коннектор к базе
        self.cursor = self.conn.cursor()  # Создаем курсор
        self.table_name = table_name
        self.create_tables()

    def create_tables(self):
        """Создаем таблицы"""
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE_NAME} (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password_salt Varchar(128), password_hash Varchar(128))"
        )
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TEXT_TABLE_NAME} (text_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), text TEXT)"
        )
        self.conn.commit()

    def row_exists(self):
        """Проверяем, есть ли строки в таблице и возвращаем нужный ответ"""
        try:
            self.cursor.execute(f"SELECT 1 FROM {self.TEXT_TABLE_NAME} LIMIT 1")
            self.cursor.execute(f"SELECT 1 FROM {self.USERS_TABLE_NAME} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False


class UserDatabase(Database):
    """Создаем класс для работы с юзером"""
    def __init__(self):
        super().__init__(self.USERS_TABLE_NAME)
        super().__init__(self.TEXT_TABLE_NAME)

    def create_user(self, user: tuple):
        """Функция создания пользователя, принимает кортеж"""
        self.create_tables()  # Создаем таблицу, если она не была еще создана

        # Делаем запрос к таблице, проверяем есть ли такой логин
        query_check_login = f"SELECT * FROM {self.USERS_TABLE_NAME} WHERE login = ?"
        self.cursor.execute(query_check_login, (user[0],))
        existing_login = self.cursor.fetchone()

        # Делаем запрос к таблице, проверяем есть ли такой email
        query_check_email = f"SELECT * FROM {self.USERS_TABLE_NAME} WHERE email = ?"
        self.cursor.execute(query_check_email, (user[1],))
        existing_email = self.cursor.fetchone()

        if existing_email or existing_login:
            return False
        # Если пользователя еще не существует, то мы передаем на хеширование пароль, а после добавляем в базу
        # логин, email и хэшированный пароль
        else:
            salt, hashed_password = hash_password(user[2])
            self.cursor.execute(f"INSERT INTO {self.USERS_TABLE_NAME} (login, email, password_salt, "
                                f"password_hash) VALUES (?, ?, ?, ?)",
                                (user[0], user[1], salt, hashed_password))
            self.cursor.execute(f"INSERT INTO {self.TEXT_TABLE_NAME} (login, email, text) VALUES "
                                "(?, ?, '')", (user[0], user[1]))
            self.conn.commit()
            return True

    def authenticate_user(self, user: tuple):
        """Аутентифицируем юзера"""
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False

        # Передаем в таблицу введенные данные от пользователя, логин или email
        query = f"SELECT password_salt, password_hash FROM {self.USERS_TABLE_NAME} WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (user[0], user[0]))
        check = self.cursor.fetchone()

        # Проверяем, если запрос check имеет данные, то проводим авторизацию и возвращаем True
        # Если в запросе в таблицу пустое значение, то возвращаем его, принимающая функция его обработает
        # Для безопасной работы мы хэшируем вновь полученный от пользователя пароли и сравниваем его с
        # сохраненным хэшированным паролем
        if check:
            salt, saved_hash = check
            check_hash = hash_password(user[1], salt)[1]
            return check_hash == user[1]

        return False

    def delete_user(self, user: tuple):
        """Удаляем пользователя"""
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False

        # Передаем в таблицу введенные данные от пользователя, логин или email
        query = f"SELECT password_salt, password_hash FROM {self.USERS_TABLE_NAME} WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (user[0], user[0]))
        check = self.cursor.fetchone()

        # Проверяем, если запрос check не имеет данных, то возвращаем False
        # Если данные по веденному логину или email есть в таблице, то начинаем работать с полученными данными
        # Для безопасной работы мы хэшируем вновь полученный от пользователя пароли и сравниваем его с
        # сохраненным хэшированным паролем. Если пароли совпадают, делаем запрос на удаление строки в базу
        if check:
            salt, saved_hash = check
            check_hash = hash_password(user[1], salt)[1]
            if saved_hash == check_hash:
                d_query = f"DELETE FROM {self.USERS_TABLE_NAME} WHERE (login = ? OR email = ?)"
                self.cursor.execute(d_query, (user[0], user[0]))
                count = self.cursor.rowcount
                self.conn.commit()
                return count > 0
        return False


class TextDatabase(Database):
    """Создаем класс для работы с текстом"""

    def __init__(self):
        super().__init__(self.TEXT_TABLE_NAME)

    def update_text(self, login: str, text: str):
        """Обновляем текст"""
        # Ищем столбец text в строке где есть введенный login
        query = f"UPDATE {self.TEXT_TABLE_NAME} SET text = ? WHERE login = ?"
        self.cursor.execute(query, (text, login))  # Передаем данные введенные пользователем
        self.conn.commit()
        return True

    def delete_text(self, login: str):
        """Удаляем текст"""
        # Ищем столбец text в строке где есть введенный login
        query_check = f"SELECT text FROM {self.TEXT_TABLE_NAME} WHERE login = ?"
        self.cursor.execute(query_check, (login,))
        text_before_del = self.cursor.fetchone()  # Сохраняем текст, который был в столбце

        # Ищем столбец text в строке где есть введенный login и обновляем его пустой строкой ""
        query = f"UPDATE {self.TEXT_TABLE_NAME} SET text = '' WHERE login = ?"
        self.cursor.execute(query, (login,))
        self.conn.commit()

        # Проверяем, существовала ли вообще строка до этого запроса и возвращаем нужный ответ
        return text_before_del[0]

    def show_text(self, login: str):
        """Выводим текст на экран"""
        # Ищем столбец text в строке где есть введенный login
        query = f"SELECT text FROM {self.TEXT_TABLE_NAME} WHERE login = ?"
        self.cursor.execute(query, (login,))
        text = self.cursor.fetchone()

        return text[0]
