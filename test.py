import io
import unittest
from unittest.mock import patch
from operation import UserOperation
import sys

class MockIoProvider:
    '''Имитируем провайдер пользовательского ввода для тестов'''
    def __init__(self, inputs):
        '''Инициализируем объект для имитации'''
        self.inputs = iter(inputs)

    def input(self, prompt):
        '''Имитируем пользовательский ввод'''
        try:
            return next(self.inputs)
        except StopIteration:
            return ""


class TestUserCreated(unittest.TestCase):
    '''Тестируем функции взаимодействия с учетной записью'''
    def setUp(self):
        '''Устанавливаем параметры тестирования'''
        self.operation = UserOperation()


    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Создания пользователя
        "test_login",  # Вводим логин
        "test_email@test.test",  # Вводим email
        "TestPass123",  # Вводим пароль
        "4",  # Выход
        "1",  # Подтверждение выхода
    ])
    def test_create_user(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем создание пользователя имитируем инпуты, передаем параметр mock_input в функцию'''
        first_expected_string = 'Пользователь успешно создан!'
        second_expected_string = 'С этим логином и почтой уже существует учетная запись'

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки
        self.operation.main()


        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == first_expected_string or result == second_expected_string, (f'При создании пользователя '
                f'возникла ошибка: {result} (ожидалось: {first_expected_string} или {second_expected_string})')


    @patch("builtins.input", side_effect=[
        "2",  # Авторизация
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_authorization_user(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем авторизации пользователя имитируем инпуты, передаем параметр mock_input в функцию'''
        first_expected_string = 'Вход успешно выполнен! Хорошего дня'
        second_expected_string = 'Неправильный логин или пароль'

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки

        self.operation.main()

        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == first_expected_string or result == second_expected_string, (f'При создании пользователя '
                f'возникла ошибка: {result} (ожидалось: {first_expected_string} или {second_expected_string})')


    @patch("builtins.input", side_effect=[
        "3",  # Удаление пользователя
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "4",  # Выход из программы
        "1"  # Подтверждение выхода
    ])
    def test_delete_user(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем удаления пользователя имитируем инпуты, передаем параметр mock_input в функцию'''
        first_expected_string = 'Пользователь успешно удален'
        second_expected_string = 'Пользователя с введенными данными не существует'

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки

        self.operation.main()

        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip() # Сохраняем выведенную строку для сравнения результата теста
        assert result == first_expected_string or result == second_expected_string, (f'При удалении пользователя '
                    f'возникла ошибка: {result} (ожидалось: {first_expected_string} или {second_expected_string})')


class TestTextCreated(unittest.TestCase):
    '''Тестируем функции обработки записи'''
    def setUp(self):
        '''Устанавливаем параметры тестирования и создаем декоратор, который создает
        пользователя перед каждым тестом, если он еще не был создан'''
        self.operation = UserOperation()
        with patch("builtins.input", side_effect=[
            "1",  # Создания пользователя
            "test_login",  # Вводим логин
            "test_email@test.test",  # Вводим email
            "TestPass123",  # Вводим пароль
            "4",  # Выход
            "1",  # Подтверждение выхода
        ]):
            self.operation.main()


    @patch("builtins.input", side_effect=[
        "1",  # Добавить запись
        "Good day!",  # Вводим запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_adding_text(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем добавление записи'''
        expected_string = 'Текст успешно обновлен!'

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки

        self.operation.main_authorize("test_login")

        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == expected_string, (f'При добавлении текста возникла ошибка: {result} '
                                           f'(ожидалось: {expected_string})')


    @patch("builtins.input", side_effect=[
        "3",  # Просмотреть запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_check_added_text(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем просмотр сохраненной записи'''
        first_expected_string = 'Good day!'
        second_expected_string = 'Запись еще не создана!'

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки

        self.operation.main_authorize("test_login")

        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == first_expected_string or result == second_expected_string, (f'При выводе текста возникла '
                                f'ошибка: {result} (ожидалось: {first_expected_string} или {second_expected_string})')


    @patch("builtins.input", side_effect=[
        "2",  # Удалить запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_delete_text(self, mock_input: unittest.mock.MagicMock):
        '''Тестируем функцию удаления записи'''
        first_expected_string = "Запись удалена!"
        second_expected_string = "Запись еще не создана!"

        output_string = io.StringIO()
        sys.stdout = output_string  # Перехватываем вывод строки

        self.operation.main_authorize("test_login")

        sys.stdout = sys.__stdout__  # Возвращаем стандартный вывод строки
        result = output_string.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == first_expected_string or result == second_expected_string, (f'При удалении текста возникла '
                                f'ошибка: {result} ожидалось: {first_expected_string} или {second_expected_string})')


if __name__ == "__main__":
    unittest.main()


