import hashlib
import os
import re
from typing import Union, Tuple

from database.database import TextDatabase, UserDatabase
from utils import generate_password


def menu() -> None:
    """Функция запуска программы и распределение запросов"""
    user_db = UserDatabase()

    query = input(
        ' Чтобы создать пользователя наберите "1".\n'
        ' Чтобы авторизоваться наберите "2".\n'
        ' Чтобы удалить учетную запись наберите "3".\n'
        ' Чтобы выйти из программы наберите "4".\n'
    )
    match query:
        case "1":
            create()

        case "2":
            user = authentication()
            if user:
                print("Вход успешно выполнен! Хорошего дня")
                return menu_authorize(user[0])

        case "3":
            user = authentication()
            if user:
                user_db.delete_user(user)
                print("Пользователь успешно удален")
                return menu()

        case _:
            return exit_program()


def create() -> Union[bool, None]:
    """Функция запроса к базе для создания пользователя"""
    user_db = UserDatabase()
    # С помощью анонимных функций создаем список кортежей, в котором указаны условия
    # к вводимым пользователем строкам
    prompts = [
        ("Введите логин: ", lambda x: len(x) > 0),
        ("Введите email: ", lambda x: re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", x)),
        ("Введите пароль (или нажмите Enter для автогенерации): ",
         lambda x: x == "" or 8 <= len(x) <= 16 and any(c.isupper() for c in x) and
                   any(c.islower() for c in x) and any(c.isdigit() for c in x))
    ]
    user = checking_values(prompts)

    # Если пользователь не указывает пароль, то запускается модуль автогенерации пароля
    if user[2] == "":
        user[2] = generate_password.choice_settings()
        print(f'Сгенерированный пароль: {user[2]}\n'
              f'Запишите его в надежное место или запомните')
    # Преобразуем список в кортеж и отправляем его в базу данных на проверку.
    # Если создание прошло успешно, возвращаем соответствущее сообщение
    user[2], salt = hash_password(user[2])
    user = tuple(user)
    check = user_db.create_user(user, salt)
    if check:
        print('Пользователь успешно создан!')
        return menu_authorize(user[0])
    print('С этим логином или почтой уже существует учетная запись')
    return menu()


def checking_values(prompts: list) -> list:
    """Функция проверки корректности введенных строк"""
    user = []
    for prompt, validation in prompts:
        while True:
            value = input(prompt)
            if validation(value):
                user.append(value)
                break
            else:
                print("Некорректное значение")
    return user


def authentication() -> Union[tuple, None]:
    """Создаем кортеж на основе введенных строк и проверяем введенные данные"""
    prompts = [
        ("Введите логин или email: ", lambda x: len(x) > 0),
        ("Введите пароль: ", lambda x: len(x) >= 8)]

    # Создаем кортеж
    user = tuple(checking_values(prompts))

    # Извлекаем из базы сохраненную соль и хэш
    database = UserDatabase()

    # Делаем проверку на существование пользователя в базе
    check = database.get_hash_and_salt(user[0])
    if check is not None:
        password_hash, salt = database.get_hash_and_salt(user[0])
        # Хэшируем пароль с помощью сохраненной соли и сравниваем с хэшем из базы
        saved_hash, _ = hash_password(user[1], salt)
        if password_hash == saved_hash:
            return user

    print("Неправильный логин или пароль")
    return menu()


def hash_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """Хэшируем пароль"""
    if salt is None:
        salt = os.urandom(16)  # Генерируем случайную соль
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Хэшируем пароль с использованием соли
    return key, salt


def exit_program() -> Union[bool, None]:
    """Функция выхода из программы"""
    ask = input(
        'Если вы хотите выйти из программы введите "1". '
        'Если хотите продолжить выполнение программы введите "2"'
    )
    if ask == "1":
        return False
    else:
        return menu()


def menu_authorize(login: str) -> Union[str, None]:
    """ Функция распределение авторизированных запросов """
    text_operation = TextOperation()
    text_db = TextDatabase()
    while True:
        query = input(
            ' Чтобы обновить запись наберите "1".\n'
            ' Чтобы добавить запись наберите "2".\n'
            ' Чтобы удалить запись наберите "3".\n'
            ' Чтобы просмотреть запись наберите "4"\n'
            ' Чтобы выйти из аккаунта наберите "5".\n'
        )
        match query:
            case "1":
                check = text_db.get_text(login)
                if check != '':
                    text_exist(login)
                else:
                    text = input("Введите новый текст: \n")
                    text_operation.update(login, text)

            case "2":
                text = input("Введите текст, который хотите добавить в запись: \n")
                text_operation.add(login, text)

            case "3":
                text_operation.delete(login)

            case "4":
                text_operation.get(login)

            case _:
                return exit_user(login)


def text_exist(login: str) -> None:
    text_operation = TextOperation()
    query = input(
        ' У вас уже сохранен текст! Если продолжить, то он будет заменен новым!\n'
        ' Наберите 1, если хотите продолжить или 2 чтобы вернуться в меню\n'
    )
    match query:
        case "1":
            text = input("Введите новый текст: \n")
            text_operation.update(login, text)

        case "2":
            return menu_authorize(login)


def exit_user(login: str) -> None:
    """Функция выхода из аккаунта"""
    ask = input(
        'Если вы хотите выйти из аккаунта введите "1". '
        'Если хотите продолжить работу введите "2"'
    )
    if ask == "1":
        return menu()
    else:
        return menu_authorize(login)


class TextOperation:
    """Операционный модуль для работы с текстом"""

    def __init__(self):
        self.text_db = TextDatabase()

    def update(self, login: str, text: str) -> None:
        """Функция обновления текста с заменой в таблицу"""
        check = self.text_db.update_text(login, text)
        if check:
            print('Текст успешно обновлен!')

    def add(self, login: str, text: str) -> None:
        """Функция добавления текста в таблицу"""
        check = self.text_db.add_text(login, text)
        if check:
            print('Текст успешно добавлен!')

    def delete(self, login: str) -> None:
        """Функция удаления текста из таблицы"""
        check = self.text_db.delete_text(login)
        if check != '':
            print('Запись удалена!')
        else:
            print('Запись еще не создана!')

    def get(self, login: str) -> None:
        """Функция вывода на просмотр сохраненного текста"""
        check = self.text_db.get_text(login)
        if check != '':
            print(check)
        else:
            print('Запись еще не создана!')
