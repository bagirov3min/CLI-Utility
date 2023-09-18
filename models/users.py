import hashlib
import os
import re
from typing import Union, Tuple

from crud.users import UserDatabase
from utils import generate_password


def create() -> Union[bool, None]:
    """Функция запроса к базе для создания пользователя"""
    database = UserDatabase()
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
    user = check_values(prompts)

    # Если пользователь не указывает пароль, то запускается модуль автогенерации пароля
    if user[2] == "":
        user[2] = generate_password.generate_password_settings()
        print(f'Сгенерированный пароль: {user[2]}\n'
              f'Запишите его в надежное место или запомните')
    # Преобразуем список в кортеж и отправляем его в базу данных на проверку.
    # Если создание прошло успешно, возвращаем соответствущее сообщение
    user[2], salt = hash_password(user[2])
    user = tuple(user)
    check = database.create_user(user, salt)
    if check:
        user_id, _, _ = database.get_hash_salt_and_user_id(user[0])
        return user_id

    return False


def check_values(prompts: list) -> list:
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


def authentication() -> Union[int, None]:
    """Создаем кортеж на основе введенных строк и проверяем введенные данные"""
    prompts = [
        ("Введите логин или email: ", lambda x: len(x) > 0),
        ("Введите пароль: ", lambda x: len(x) >= 8)]

    # Создаем кортеж
    user = tuple(check_values(prompts))

    # Извлекаем из базы сохраненную соль и хэш
    database = UserDatabase()

    # Делаем проверку на существование пользователя в базе
    check = database.get_hash_salt_and_user_id(user[0])
    if check is not None:
        user_id, password_hash, salt = database.get_hash_salt_and_user_id(user[0])
        # Хэшируем пароль с помощью сохраненной соли и сравниваем с хэшем из базы
        saved_hash, _ = hash_password(user[1], salt)
        if password_hash == saved_hash:
            return user_id

    print("Неправильный логин или пароль")
    return False


def hash_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """Хэшируем пароль"""
    if salt is None:
        salt = os.urandom(16)  # Генерируем случайную соль
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Хэшируем пароль с использованием соли
    return key, salt


def check_int() -> int:
    while True:
        try:
            text_id = int(input("Введите номер текста: \n"))
            break
        except ValueError:
            print("Вы ввели некорректное значение. Пожалуйста, введите целое число.")
    return text_id
