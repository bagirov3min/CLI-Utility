import sqlite3


class Database:
    """Работаем с базой данных"""
    USERS_TABLE_NAME = "users_table"
    TEXT_TABLE_NAME = "notes_table"

    def __init__(self, table_name: str) -> None:
        """Указываем параметры работы для с базой данных"""
        self.conn = sqlite3.connect("records.sqlite")  # Создаем коннектор к базе
        self.cursor = self.conn.cursor()  # Создаем курсор
        self.table_name = table_name
        self.create_tables()

    def create_tables(self) -> None:
        """Создаем таблицы"""
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE_NAME} (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password_hash Varchar(128), password_salt Varchar(128))"
        )
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.TEXT_TABLE_NAME} ("
            "text_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER,"
            "text TEXT,"
            f"FOREIGN KEY (user_id) REFERENCES {self.USERS_TABLE_NAME}(user_id))"
        )
        self.conn.commit()

    def row_exists(self) -> bool:
        """Проверяем, есть ли строки в таблице и возвращаем нужный ответ"""
        try:
            self.cursor.execute(f"SELECT 1 FROM {self.TEXT_TABLE_NAME} LIMIT 1")
            self.cursor.execute(f"SELECT 1 FROM {self.USERS_TABLE_NAME} LIMIT 1")
            return True
        except sqlite3.OperationalError:
            return False






