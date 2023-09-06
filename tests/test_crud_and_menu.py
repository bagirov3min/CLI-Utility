import io
import unittest
from unittest.mock import patch
from utils.menu import menu, menu_authorize


class MockIoProvider:
    """Имитируем провайдер пользовательского ввода для тестов"""

    def __init__(self, inputs: list[str]) -> None:
        """Инициализируем объект для имитации"""
        self.inputs = iter(inputs)

    def input(self, prompt: str) -> str:
        """Имитируем пользовательский ввод"""
        try:
            return next(self.inputs)
        except StopIteration:
            return ""


class TestUserCreated(unittest.TestCase):
    """Тестируем функции взаимодействия с учетной записью"""

    def setUp(self) -> None:
        """Устанавливаем параметры тестирования"""
        self.main_menu = menu

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Создания пользователя
        "test_login",  # Вводим логин
        "test_email@test.test",  # Вводим email
        "TestPass123",  # Вводим пароль
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_create_user(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем создание пользователя"""
        expected_list = ['Пользователь успешно создан!', 'С этим логином и почтой уже существует учетная запись']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "2",  # Авторизация
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_authorization_user(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем авторизации пользователя"""
        expected_list = ['Вход успешно выполнен! Хорошего дня', 'Неправильный логин или пароль']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "3",  # Удаление пользователя
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_delete_user(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем удаления пользователя"""
        expected_list = ['Пользователь успешно удален', 'Пользователя с введенными данными не существует']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'


class TestTextCreated(unittest.TestCase):
    """Тестируем функции обработки записи"""

    def setUp(self) -> None:
        """Устанавливаем параметры тестирования и создаем декоратор, который создает
        пользователя перед каждым тестом, если он еще не был создан"""
        self.main_menu = menu
        self.main_menu_authorize = menu_authorize

        with patch("builtins.input", side_effect=[  # Устанавливаем стартовые значения инпутов для всех функций
            "1",  # Создания пользователя
            "test_login",  # Вводим логин
            "test_email@test.test",  # Вводим email
            "TestPass123",  # Вводим пароль
            "5",  # Выход из аккаунта
            "1",  # Подтверждение выхода
            "4",  # Выход из программы
            "1",  # Подтверждение выхода
        ]):
            self.main_menu()

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Обновить запись
        "Good",  # Вводим запись
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_update_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем добавление записи"""
        expected_string = 'Текст успешно обновлен!'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == expected_string, (
            f'При добавлении текста возникла ошибка: {result} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "2",  # Добавить запись
        " day!",  # Вводим запись
        "4"  # Просмотреть запись
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_added_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем добавление записи"""
        expected_string = 'Текст успешно добавлен!'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result == expected_string, (
            f'При добавлении текста возникла ошибка: {result} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "3",  # Удалить запись
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_delete_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем функцию удаления записи"""
        expected_list = ["Запись удалена!", "Запись еще не создана!"]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "4",  # Просмотреть запись
        "5",  # Выход из аккаунта
        "1",  # Подтверждение выхода
        "4",  # Выход из программы
        "1",  # Подтверждение выхода
    ])
    def test_check_added_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем просмотр сохраненной записи"""
        expected_list = ['Good day!', 'Запись еще не создана!', 'Good ', 'day!']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            menu_authorize("test_login")

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'


if __name__ == "__main__":
    unittest.main()
