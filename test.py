import io
import unittest
from unittest.mock import patch
from operation import menu, menu_authorize


class MockIoProvider:
    """Имитируем провайдер пользовательского ввода для тестов"""

    def __init__(self, inputs):
        """Инициализируем объект для имитации"""
        self.inputs = iter(inputs)

    def input(self, prompt):
        """Имитируем пользовательский ввод"""
        try:
            return next(self.inputs)
        except StopIteration:
            return ""


class TestUserCreated(unittest.TestCase):
    """Тестируем функции взаимодействия с учетной записью"""

    def setUp(self):
        """Устанавливаем параметры тестирования"""
        self.main_menu = menu

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Создания пользователя
        "test_login",  # Вводим логин
        "test_email@test.test",  # Вводим email
        "TestPass123",  # Вводим пароль
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_create_user(self, mock_input: unittest.mock.MagicMock):
        """Тестируем создание пользователя имитируем инпуты, передаем параметр mock_input в функцию"""
        first_expected_string = 'Пользователь успешно создан!'
        second_expected_string = 'С этим логином и почтой уже существует учетная запись'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == first_expected_string or result == second_expected_string, (
            f'При создании пользователя возникла ошибка: {result} '
            f'(ожидалось: {first_expected_string} или {second_expected_string})'
        )

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
        """Тестируем авторизации пользователя имитируем инпуты, передаем параметр mock_input в функцию"""
        first_expected_string = 'Вход успешно выполнен! Хорошего дня'
        second_expected_string = 'Неправильный логин или пароль'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == first_expected_string or result == second_expected_string, (
            f'При создании пользователя возникла ошибка: {result} '
            f'(ожидалось: {first_expected_string} или {second_expected_string})'
        )

    @patch("builtins.input", side_effect=[
        "3",  # Удаление пользователя
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_delete_user(self, mock_input: unittest.mock.MagicMock):
        """Тестируем удаления пользователя имитируем инпуты, передаем параметр mock_input в функцию"""
        first_expected_string = 'Пользователь успешно удален'
        second_expected_string = 'Пользователя с введенными данными не существует'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == first_expected_string or result == second_expected_string, (
            f'При удалении пользователя возникла ошибка: {result} '
            f'(ожидалось: {first_expected_string} или {second_expected_string})'
        )


class TestTextCreated(unittest.TestCase):
    """Тестируем функции обработки записи"""

    def setUp(self):
        """Устанавливаем параметры тестирования и создаем декоратор, который создает
        пользователя перед каждым тестом, если он еще не был создан"""
        self.main_menu = menu
        self.main_menu_authorize = menu_authorize

        with patch("builtins.input", side_effect=[
            "1",  # Создания пользователя
            "test_login",  # Вводим логин
            "test_email@test.test",  # Вводим email
            "TestPass123",  # Вводим пароль
            "4",  # Выход из аккаунта
            "1",  # Подтверждение выхода
            "4",  # Выход из программы
            "1",  # Подтверждение выхода
        ]):
            self.main_menu()

    @patch("builtins.input", side_effect=[
        "1",  # Добавить запись
        "Good day!",  # Вводим запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_adding_text(self, mock_input: unittest.mock.MagicMock):
        """Тестируем добавление записи"""
        expected_string = 'Текст успешно обновлен!'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == expected_string, (
            f'При добавлении текста возникла ошибка: {result} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[
        "3",  # Просмотреть запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_check_added_text(self, mock_input: unittest.mock.MagicMock):
        """Тестируем просмотр сохраненной записи"""
        first_expected_string = 'Good day!'
        second_expected_string = 'Запись еще не создана!'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == first_expected_string or result == second_expected_string, (
            f'При выводе текста возникла ошибка: {result} '
            f'(ожидалось: {first_expected_string} или {second_expected_string})'
        )

    @patch("builtins.input", side_effect=[
        "2",  # Удалить запись
        "4",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_delete_text(self, mock_input: unittest.mock.MagicMock):
        """Тестируем функцию удаления записи"""
        first_expected_string = "Запись удалена!"
        second_expected_string = "Запись еще не создана!"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        print(result)
        assert result == first_expected_string or result == second_expected_string, (
            f'При удалении текста возникла ошибка: {result} '
            f'ожидалось: {first_expected_string} или {second_expected_string})'
        )


if __name__ == "__main__":
    unittest.main()
