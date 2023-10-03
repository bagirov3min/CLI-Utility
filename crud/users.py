import sqlite3
from typing import Union

from database.session import Database


class User:
    """Создаем класс для работы с юзером"""

    USERS_TABLE_NAME = "users_table"
    TEXT_TABLE_NAME = "notes_table"
    CREATE_TABLE = Database

    def __init__(self) -> None:
        self.conn = sqlite3.connect("records.sqlite")  # Создаем коннектор к базе
        self.cursor = self.conn.cursor()  # Создаем курсор
        self.CREATE_TABLE().create_tables()  # Создаем таблицу, если она не была еще создана

    def create_user(self, user: tuple) -> bool:
        """Функция создания пользователя, принимает кортеж"""
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
            self.cursor.execute(f"INSERT INTO {self.USERS_TABLE_NAME} (login, email, password_hash) VALUES"
                                f" (?, ?, ?)", (user[0], user[1], user[2]))
            self.conn.commit()
            return True

    def authenticate_user(self, user: tuple) -> bool:
        """Аутентифицируем юзера"""
        check = self.get_hash(user[0])

        # Проверяем, если запрос check имеет данные, то проводим авторизацию и возвращаем True
        # Если в запросе в таблицу пустое значение, то возвращаем его, принимающая функция его обработает
        if check:
            return check == user[1]

        return False

    def delete_user(self, user_id: int) -> bool:
        """Удаляем пользователя"""

        # Проверяем, если запрос check не имеет данных, то возвращаем False
        # Если данные по веденному логину или email есть в таблице, то проверяем сохраненный кэш с вновь полученным
        # Если хэши совпадают, делаем запрос на удаление строки в базу
        d_query = f"DELETE FROM {self.USERS_TABLE_NAME} WHERE user_id = ?"
        query = f"DELETE FROM {self.TEXT_TABLE_NAME} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()
        self.cursor.execute(d_query, (user_id,))
        count = self.cursor.rowcount
        self.conn.commit()
        return count > 0

    def get_hash(self, login: str) -> Union[bool, bytes]:
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False
        # Передаем в таблицу введенные данные от пользователя, логин или email
        query = f"SELECT password_hash FROM {self.USERS_TABLE_NAME} WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (login, login))
        return self.cursor.fetchone()

    def get_hash_and_user_id(self, login: str) -> Union[bool, bytes]:
        """ Получаем хэш и id user"""
        if not self.row_exists():  # Если в таблице нет столбцов вернет False
            return False
        query = f"SELECT user_id, password_hash FROM {self.USERS_TABLE_NAME} WHERE (login = ? OR email = ?)"
        self.cursor.execute(query, (login, login))
        return self.cursor.fetchone()

    def row_exists(self) -> bool:
        """Проверяем, есть ли строки в таблице и возвращаем нужный ответ"""
        try:
            self.cursor.execute(f"SELECT 1 FROM {self.TEXT_TABLE_NAME} LIMIT 1")
            self.cursor.execute(f"SELECT 1 FROM {self.USERS_TABLE_NAME} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False
