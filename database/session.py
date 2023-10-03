import sqlite3


class Database:
    """Работаем с базой данных"""
    USERS_TABLE_NAME = "users_table"
    TEXT_TABLE_NAME = "notes_table"

    def __init__(self) -> None:
        """Указываем параметры работы с базой данных"""
        self.conn = sqlite3.connect("records.sqlite")  # Создаем коннектор к базе
        self.cursor = self.conn.cursor()  # Создаем курсор
        self.create_tables()

    def create_tables(self) -> None:
        """Создаем таблицы"""
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE_NAME} (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password_hash Varchar(128))"
        )
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TEXT_TABLE_NAME} ("
            "text_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER,"
            "text TEXT,"
            f"FOREIGN KEY (user_id) REFERENCES {self.USERS_TABLE_NAME}(user_id) ON DELETE CASCADE)"
        )
        self.conn.commit()