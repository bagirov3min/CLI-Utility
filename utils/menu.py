from typing import Union

from crud.records import Text
from crud.users import User
from models.records import TextModel
from models.users import create, authentication, check_int


def main_menu() -> Union[int, None]:
    """Функция запуска программы и распределение запросов"""
    user_db = User()

    query = input(
        ' Чтобы создать пользователя наберите "1".\n'
        ' Чтобы авторизоваться наберите "2".\n'
        ' Чтобы удалить учетную запись наберите "3".\n'
        ' Чтобы выйти из программы наберите "4".\n'
    )
    match query:
        case "1":
            user_id = create()
            if user_id:
                print('Пользователь успешно создан!')
                user_menu(user_id)
            else:
                print('С этим логином или почтой уже существует учетная запись')
                return main_menu()

        case "2":
            user_id = authentication()
            if user_id:
                print("Вход успешно выполнен! Хорошего дня")
                return user_menu(user_id)
            else:
                return main_menu()

        case "3":
            user_id = authentication()
            if user_id:
                user_db.delete_user(user_id)
                print("Пользователь успешно удален")
                return main_menu()

        case _:
            return close()


def user_menu(user_id: int) -> Union[str, None, bool]:
    """ Функция распределение авторизированных запросов """
    text_model = TextModel()
    text_db = Text()
    while True:

        all_record = text_db.get_text_all(user_id)
        if len(all_record) > 0:
            print("Ваши записи:")
            for record in all_record:
                print('№', record[0], ':', sep='', end=' ')
                print(record[1])
        else:
            print("У вас еще нет ни одной записи")

        query = input(
            ' Чтобы добавить запись наберите "1".\n'
            ' Чтобы редактировать запись наберите "2".\n'
            ' Чтобы удалить запись наберите "3".\n'
            ' Чтобы удалить все записи наберите "4"\n'
            ' Чтобы выйти из аккаунта наберите "5".\n'
            ' Чтобы выйти из программы наберите "6".\n'
        )
        match query:
            case "1":
                text = input("Введите новый текст: \n")
                text_model.add(user_id, text)

            case "2":
                text_id = check_int()
                text = input("Введите текст, который хотите добавить: \n")
                text_model.update(text_id, text)

            case "3":
                text_id = check_int()
                text_model.delete(text_id)

            case "4":
                text_model.delete_all(user_id)

            case "5":
                return logout(user_id)

            case _:
                ask = input(
                    'Если вы хотите выйти из программы введите "1". '
                    'Если хотите продолжить работу введите "2"'
                )
                if ask == "1":
                    return False
                else:
                    continue


def logout(user_id: int) -> None:
    """Функция выхода из аккаунта"""
    ask = input(
        'Если вы хотите выйти из аккаунта введите "1". '
        'Если хотите продолжить работу введите "2"'
    )
    if ask == "1":
        return main_menu()
    else:
        return user_menu(user_id)


def close() -> Union[bool, None]:
    """Функция выхода из программы"""
    ask = input(
        'Если вы хотите выйти из программы введите "1". '
        'Если хотите продолжить выполнение программы введите "2"'
    )
    if ask == "1":
        return False
    else:
        return main_menu()
