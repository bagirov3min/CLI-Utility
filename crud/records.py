import sqlite3
from typing import Union

from database.session import Database


class TextDatabase(Database):
    """Создаем класс для работы с текстом"""

    def __init__(self) -> None:
        super().__init__(self.TEXT_TABLE_NAME)

    def add_text(self, user_id: int, text: str) -> bool:
        """Обновляем текст"""
        # Ищем столбец text в строке где есть введенный login
        query = f"INSERT OR REPLACE INTO {self.TEXT_TABLE_NAME} (user_id, text) VALUES (?, ?)"
        self.cursor.execute(query, (user_id, text))  # Передаем данные введенные пользователем
        self.conn.commit()
        return True

    def update_text(self, text_id: int, text: str) -> bool:
        """Добавляем текст"""
        # Проверяем, существует ли запись с указанным text_id
        check_query = f"SELECT COUNT(*) FROM {self.TEXT_TABLE_NAME} WHERE text_id = ?"
        self.cursor.execute(check_query, (text_id,))
        count = self.cursor.fetchone()[0]

        if count == 0:
            # Записи с указанным text_id не существует, возвращаем False
            return False

        # Ищем столбец text в строке где есть введенный login
        query = f"UPDATE {self.TEXT_TABLE_NAME} SET  text = text || ? WHERE text_id = ?"
        self.cursor.execute(query, (text, text_id))  # Передаем данные введенные пользователем
        self.conn.commit()
        return True

    def delete_text(self, text_id: int) -> str:
        """Удаляем текст"""
        # Ищем столбец text в строке где есть введенный user_id
        query_check = f"SELECT text FROM {self.TEXT_TABLE_NAME} WHERE text_id = ?"
        self.cursor.execute(query_check, (text_id,))
        text_before_del = self.cursor.fetchone()  # Сохраняем текст, который был в столбце

        # Ищем столбец text в строке где есть введенный user_id и удаляем его
        query = f"DELETE FROM {self.TEXT_TABLE_NAME} WHERE text_id = ?"
        self.cursor.execute(query, (text_id,))
        self.conn.commit()

        # Проверяем, существовала ли вообще строка до этого запроса и возвращаем нужный ответ
        return text_before_del

    def delete_all(self, user_id: int) -> list:
        """Удаляем все записи"""
        # Ищем столбцы text в строках с user_id
        query_check = f"SELECT text FROM {self.TEXT_TABLE_NAME} WHERE user_id =?"
        self.cursor.execute(query_check, (user_id, ))
        text_before_del = self.cursor.fetchall()

        # Ищем столбцы text в строках где есть user_id и удаляем их
        query = f"DELETE FROM {self.TEXT_TABLE_NAME} WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

        # Проверяем, существовала ли вообще строка до этого запроса и возвращаем нужный ответ
        return text_before_del

    def read_text(self, user_id: int) -> str:
        """Выводим текст на экран"""
        # Ищем столбец text в строке где есть введенный login
        query = f"SELECT text FROM {self.TEXT_TABLE_NAME} WHERE (user_id = ? and text_id = ?)"
        with sqlite3.connect("records.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            text = cursor.fetchone()
            if text:
                return text[0]
            return ""

    def get_text(self, user_id: int) -> Union[list, None]:
        """ Получаем тексты по user_id """
        # Ищем столбец text в строке где есть введенный login
        query = f"SELECT text_id, text FROM {self.TEXT_TABLE_NAME} WHERE user_id = ?"
        with sqlite3.connect("records.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            try:
                result = cursor.fetchall()
                return result

            except sqlite3.OperationalError:
                return None