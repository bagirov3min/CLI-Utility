import re
import generate_password
from database import EditTable


class UserOperation:
    '''Создаем операционный модуль'''
    def __init__(self):
        '''Указываем параметры для модуля'''
        self.table = EditTable()


    def main(self):
        ''' Функция запуска программы и распределение запросов '''
        query = input(
            ' Чтобы создать пользователя наберите "1".\n'
            ' Чтобы авторизоваться наберите "2".\n'
            ' Чтобы удалить учетную запись наберите "3".\n'
            ' Чтобы выйти из программы наберите "4".\n'
        )
        match query:
            case "1":
                return self.create_user()
            case "2":
                return self.authorization()
            case "3":
                return self.delete_user()
            case _:
                return self.exit_programm()


    def main_authorize(self, login: str):
        ''' Функция распределение авторизированных запросов '''
        while True:
            query = input(
                ' Чтобы добавить запись наберите "1".\n'
                ' Чтобы удалить запись наберите "2".\n'
                ' Чтобы просмотреть запись наберите "3"\n'
                ' Чтобы выйти из аккаунта наберите "4".\n'
            )
            match query:
                case "1":
                    text = input("Введите текст, который хотите добавить в запись': \n")
                    return self.table.update_text(login, text)
                case "2":
                    return self.table.delete_text(login)
                case "3":
                    return self.table.show_text(login)
                case _:
                    return self.exit_user(login)


    def create_user(self):
        '''Функция запроса к базе для создания пользователя'''
        # С помощью анонимных функций создаем список кортежей, в котором указаны условия
        # к вводимым пользователем строкам
        promts = [
            ("Введите логин: ", lambda x: len(x) > 0),
            ("Введите email: ", lambda x: re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", x)),
            ("Введите пароль (или нажмите Enter для автогенерации): ", lambda x: x == "" or len(x) >= 8 and
            len(x) <= 16 and any(c.isupper() for c in x) and any(c.islower() for c in x) and
            any(c.isdigit() for c in x))
        ]
        user = self.checking_values(promts)

        # Если пользователь не указывает пароль, то запускается модуль автогенерации пароля
        if user[2] == "":
            user[2] = generate_password.pass_choice()
            print(f'Сгенерированный пароль: {user[2]}\n'
                  f'Запишите его в надежное место или запомните')
        user = tuple(user)
        self.table.create_user_database(user)
        self.main()


    def initialization(self):
        '''Функция проверки корректности вводимых строк'''
        promts = [
            ("Введите логин или email: ", lambda x: len(x) > 0),
            ("Введите пароль: ", lambda x: len(x) >= 8)]
        user = tuple(self.checking_values(promts))
        return user


    def authorization(self):
        '''Функция запроса к базе для авторизации пользователя'''
        # Передаем введенные строки пользователя в функцию корректности
        # далее передаем эти данные в базу и ждем ответа.
        user = self.initialization()
        check = self.table.authenticate_user(user)
        if check:
            print("Вход успешно выполнен! Хорошего дня")
            return self.main_authorize(user[0])
        else:
            print("Неправильный логин или пароль")
            return self.main()


    def delete_user(self):
        '''Функция запроса к базе для удаления пользователя'''
        # Передаем введенные строки пользователя в функцию корректности
        # далее передаем эти данные в базу и ждем ответа.
        user = self.initialization()
        check = self.table.delete_user_database(user)
        if check:
            print("Пользователь успешно удален")
        else:
            print("Пользователя с введенными данными не существует")
        return self.main()


    def exit_programm(self):
        '''Функция выхода из программы'''
        ask = input(
            'Если вы хотите выйти из программы введите "1". '
            'Если хотите продолжить выполнение программы введите "2"'
        )
        if ask == "1":
            return False
        else:
            return self.main()


    def exit_user(self, login: str):
        '''Функция выхода из аккаунта'''
        ask = input(
            'Если вы хотите выйти из аккаунта введите "1". '
            'Если хотите продолжить работу введите "2"'
        )
        if ask == "1":
            return self.main()
        else:
            return self.main_authorize(login)


    def checking_values(self, prompts: list):
        '''Функция проверки корректности введенных строк на основе
        параметров указанных в анонимных функциях'''
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

