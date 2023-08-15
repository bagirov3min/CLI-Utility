from create_database import create_user_, authorization_, delete_user_


def main():
    ask = input(
        'Чтобы создать пользователя наберите "1". Чтобы авторизоваться наберите "2". Чтобы удалить учетную запись наберите "3". Чтобы выйти из программы наберите "4".'
    )
    if ask.lower() == "1":
        return create_user()
    elif ask.lower() == "2":
        return authorization()
    elif ask.lower() == "3":
        return delete_user()
    else:
        return exit_programm()


def initilization():
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
    return user


def create_user():
    user = initilization()
    create_user_(user)
    print("Аккаунт успешно создан!")


def authorization():
    user = initilization()
    check = authorization_(user)
    if check:
        print("Вход успешно выполнен! Хорошего дня")
    else:
        print("Неправильный логин или пароль")


def delete_user():
    user = initilization()
    check = delete_user_(user)
    if check:
        print("Пользователь успешно удален")
    else:
        print("Пользователя с введенными данными не существует")


def exit_programm():
    ask = input(
        'Если вы хотите выйти из программы введите "1". Если хотите продолжить выполнение программы введите "2"'
    )
    if ask == "1":
        return False
    else:
        return main()


main()
