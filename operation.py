import re
import generate_password
from database import EditTable

class UserOperation:
    def __init__(self):
        self.table = EditTable()

    def main(self):
        ''' Функция запуска рограммы и распределение запросов '''
        ask = input(
            'Чтобы создать пользователя наберите "1".\n'
            ' Чтобы авторизоваться наберите "2".\n'
            ' Чтобы удалить учетную запись наберите "3".\n'
            ' Чтобы выйти из программы наберите "4".\n'
        )
        if ask == "1":
            return self.create_user()
        elif ask == "2":
            return self.authorization()
        elif ask == "3":
            return self.delete_user()
        else:
            return self.exit_programm()

    def main_authorize(self, login):
        ''' Функция запуска рограммы и распределение запросов '''
        while True:
            ask = input(
                'Чтобы добавить запись наберите "1".\n'
                ' Чтобы удалить запись наберите "2".\n'
                ' Чтобы просмотреть запись наберите "3"\n'
                ' Чтобы выйти из аккаунта наберите "4".\n'
            )
            if ask == "1":
                text = input("Введите текст, который хотите добавить в запись': \n")
                self.table.update_text(login, text)
            elif ask == "2":
                self.table.delete_text(login)
            elif ask == "3":
                self.table.show_text(login)
            else:
                return self.exit_user(login)



    def create_user(self):
        '''Функция запроса к базе для создания пользователя'''
        promts = [
            ("Введите логин: ", lambda x: len(x) > 0),
            ("Введите email: ", lambda x: re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", x)),
            ("Введите пароль (или нажмите Enter для автогенерации): ", lambda x: x == "" or len(x) >= 8 and
            any(c.isupper() for c in x) and any(c.islower() for c in x) and any(c.isdigit() for c in x))
        ]
        user = self.checking_values(promts)
        if user[2] == "":
            user[2] = generate_password.pass_choice()
            print(f'Сгенерированный пароль: {user[2]}\n'
                  f'Запишите его в надежное место или запомните')
        user = tuple(user)
        self.table.create_user_database(user)
        return self.main()

    def initilization(self):
        '''Функция запроса к базе для входа пользователя'''
        promts = [
            ("Введите логин или email: ", lambda x: len(x) > 0),
            ("Введите пароль: ", lambda x: len(x) >= 8)]
        user = tuple(self.checking_values(promts))
        return user[0], user[1]



    def authorization(self):
        '''Функция запроса к базе для авторизации пользователя'''
        login_or_email, password = self.initilization()
        check = self.table.authenticate_user(login_or_email, password)
        if check:
            print("Вход успешно выполнен! Хорошего дня")
            return self.main_authorize(login_or_email)
        else:
            print("Неправильный логин или пароль")
            return self.main()


    def delete_user(self):
        '''Функция запроса к базе для удаления пользователя'''
        login_or_email, password = self.initilization()
        check = self.table.delete_user_database(login_or_email, password)
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

    def exit_user(self, login):
        '''Функция выхода из программы'''
        ask = input(
            'Если вы хотите выйти из аккаунта введите "1". '
            'Если хотите продолжить работу введите "2"'
        )
        if ask == "1":
            return self.main()
        else:
            return self.main_authorize(login)

    def checking_values(self, prompts):
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

