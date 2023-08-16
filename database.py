import sqlite3



class EditTable:
    def __init__(self):
        self.conn = sqlite3.connect("users.sqlite")
        self.cursor = self.conn.cursor()
    def create_table(self):
        '''Функция создания таблицы'''
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " login Varchar(32), email Varchar(32), password Varchar(32), text TEXT)"
        )
        self.conn.commit()
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
            self.cursor.execute("INSERT INTO users (login, email, password, text) VALUES (?, ?, ?, '')", user)
            self.conn.commit()
            print('Пользователь успешно создан!')


    def authenticate_user(self, login_or_email, password):
        '''Функция авторизации пользователя'''
        try:
            self.cursor.execute("SELECT 1 FROM users LIMIT 1")
        except sqlite3.OperationalError:
            return False

        query = "SELECT * FROM users WHERE (login = ? OR email = ?) AND password = ?"

        if "@" in login_or_email and '.' in login_or_email:
            params = (login_or_email, login_or_email, password)
        else:
            params = (login_or_email, login_or_email, password)

        self.cursor.execute(query, params)
        user_data = self.cursor.fetchone()
        return user_data


    def delete_user_database(self, login_or_email, password):
        '''Функция удаления пользователя'''
        try:
            self.cursor.execute("SELECT 1 FROM users LIMIT 1")
        except sqlite3.OperationalError:
            return False

        query = "DELETE FROM users WHERE (login = ? OR email = ?) AND password = ?"

        if "@" in login_or_email and '.' in login_or_email:
            params = (login_or_email, login_or_email, password)
        else:
            params = (login_or_email, login_or_email, password)

        self.cursor.execute(query, params)
        count = self.cursor.rowcount
        self.conn.commit()
        return count > 0

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

