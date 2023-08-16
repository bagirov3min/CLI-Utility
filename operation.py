from database import EditTable

class UserOperation:
    table = EditTable()
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
                print('Введите текст, который хотите добавить в запись')
                text = input()
                self.table.update_text(login, text)
            elif ask == "2":
                self.table.delete_text(login)
            elif ask == "3":
                self.table.show_text(login)
            else:
                return self.exit_user(login)



    def create_user(self):
        '''Функция запроса к базе для создания пользователя'''
        login = input("Введите логин: ")
        while len(login) == 0:
            print("Поле логин не может быть пустым!")
            login = input("Введите логин: ")
        email = input("Введите email: ")
        while "@" not in email or "." not in email:
            print("Введенн некорректный email!")
            email = input("Введите email: ")
        password = input("Введите пароль: ")
        while len(password) < 8:
            print("Длина пароля не может составлять менее 8 символов!")
            password = input("Введите пароль: ")
        user = (login, email, password)
        self.table.create_user_database(user)
        return self.main()

    def initilization(self):
        '''Функция запроса к базе для входа пользователя'''
        login_or_email = input("Введите логин или email: ")
        while len(login_or_email) == 0:
            print("Поле не может быть пустым!")
            login_or_email = input("Введите логин: ")
        password = input("Введите пароль: ")
        while len(password) < 8:
            print("Длина пароля не может составлять менее 8 символов!")
            password = input("Введите пароль: ")
        return login_or_email, password



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
