import re
import generate_password
from database import TextDatabase, UserDatabase


def menu():
    """Функция запуска программы и распределение запросов"""
    user_operation = UserOperation()

    query = input(
        ' Чтобы создать пользователя наберите "1".\n'
        ' Чтобы авторизоваться наберите "2".\n'
        ' Чтобы удалить учетную запись наберите "3".\n'
        ' Чтобы выйти из программы наберите "4".\n'
    )
    match query:
        case "1":
            check = user_operation.create()
            if check is not None:
                return check
        case "2":
            check = user_operation.authenticate()
            if check is not None:
                return check
        case "3":
            check = user_operation.delete()
            if check is not None:
                return check
        case _:
            return exit_program()


def menu_authorize(login: str):
    """ Функция распределение авторизированных запросов """
    text_operation = TextOperation()

    while True:
        query = input(
            ' Чтобы добавить запись наберите "1".\n'
            ' Чтобы удалить запись наберите "2".\n'
            ' Чтобы просмотреть запись наберите "3"\n'
            ' Чтобы выйти из аккаунта наберите "4".\n'
        )
        match query:
            case "1":
                text_operation.update(login)
            case "2":
                text_operation.delete(login)
            case "3":
                text_operation.show(login)
            case _:
                return exit_user(login)


def initialization():
    """Функция создания кортежа на основе введенных строк"""
    prompts = [
        ("Введите логин или email: ", lambda x: len(x) > 0),
        ("Введите пароль: ", lambda x: len(x) >= 8)]
    user = tuple(checking_values(prompts))
    return user


def checking_values(prompts: list):
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


def exit_program():
    """Функция выхода из программы"""
    ask = input(
        'Если вы хотите выйти из программы введите "1". '
        'Если хотите продолжить выполнение программы введите "2"'
    )
    if ask == "1":
        return False
    else:
        return menu()


def exit_user(login: str):
    """Функция выхода из аккаунта"""
    ask = input(
        'Если вы хотите выйти из аккаунта введите "1". '
        'Если хотите продолжить работу введите "2"'
    )
    if ask == "1":
        return menu()
    else:
        return menu_authorize(login)


class UserOperation:
    """Создаем операционный модуль для работы с юзером"""

    def __init__(self):
        self.user_db = UserDatabase()

    def create(self):
        """Функция запроса к базе для создания пользователя"""
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
        user = tuple(user)
        check = self.user_db.create_user(user)
        if check:
            print('Пользователь успешно создан!')
            return menu_authorize(user[0])
        else:
            print('С этим логином и почтой уже существует учетная запись')
            return False

    def authenticate(self):
        """Функция запроса к базе для авторизации пользователя"""
        # Передаем введенные строки пользователя в функцию корректности
        # далее передаем эти данные в базу и ждем ответа.
        user = initialization()
        check = self.user_db.authenticate_user(user)
        if check:
            print("Вход успешно выполнен! Хорошего дня")
            return menu_authorize(user[0])
        else:
            print("Неправильный логин или пароль")
            return menu()

    def delete(self):
        """Функция запроса к базе для удаления пользователя"""
        # Передаем введенные строки пользователя в функцию корректности
        # далее передаем эти данные в базу и ждем ответа.
        user = initialization()
        check = self.user_db.delete_user(user)
        if check:
            print("Пользователь успешно удален")
        else:
            print("Пользователя с введенными данными не существует")
        return menu()


class TextOperation:
    """Создаем операционный модуль для работы с текстом"""

    def __init__(self):
        self.text_db = TextDatabase()

    def update(self, login: str):
        """Создаем функцию добавления текста в таблицу"""
        text = input("Введите текст, который хотите добавить в запись': \n")

        check = self.text_db.update_text(login, text)
        if check:
            print('Текст успешно обновлен!')

    def show(self, login: str):
        """Создаем функцию вывода на просмотр сохраненного текста"""
        check = self.text_db.show_text(login)
        if check != '':
            print(check)
        else:
            print('Запись еще не создана!')

    def delete(self, login: str):
        """Создаем функцию удаления текста из таблицы"""
        check = self.text_db.delete_text(login)
        if check != '':
            print('Запись удалена!')
        else:
            print('Запись еще не создана!')