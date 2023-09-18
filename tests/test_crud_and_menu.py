import io
import unittest
from unittest.mock import patch
from utils.menu import main_menu, user_menu


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
        self.main_menu = main_menu

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Создания пользователя
        "test_login",  # Вводим логин
        "test_email@test.test",  # Вводим email
        "TestPass123",  # Вводим пароль
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_create_user(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем создание пользователя"""
        expected_list = ['Пользователь успешно создан!', 'С этим логином или почтой уже существует учетная запись',
                         'У вас еще нет ни одной записи ']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            main_menu()

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "2",  # Авторизация
        "test_login",  # Вводим логин
        "TestPass123",  # Вводим пароль
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_authorization_user(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем авторизации пользователя"""
        expected_list = ['Вход успешно выполнен! Хорошего дня', 'Неправильный логин или пароль',
                         'У вас еще нет ни одной записи']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            main_menu()

        result = mock_output.getvalue().strip().split()  # Сохраняем выведенную строку для сравнения результата теста
        result = ' '.join(result[-7:])
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
        expected_list = ['Пользователь успешно удален', 'Пользователя с введенными данными не существует',
                         'Неправильный логин или пароль']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            main_menu()

        result = mock_output.getvalue().strip().split()  # Сохраняем выведенную строку для сравнения результата теста
        result = ' '.join(result[-7:])
        assert result in expected_list, f'При выводе текста возникла ошибка: {result} (ожидалось: {expected_list})'


class TestTextCreated(unittest.TestCase):
    """Тестируем функции обработки записи"""

    def setUp(self) -> None:
        """Устанавливаем параметры тестирования и создаем декоратор, который создает
        пользователя перед каждым тестом, если он еще не был создан"""
        self.main_menu = main_menu
        self.user_menu = user_menu

        with patch("builtins.input", side_effect=[  # Устанавливаем стартовые значения инпутов для всех функций
            "1",  # Создания пользователя
            "test_login",  # Вводим логин
            "test_email@test.test",  # Вводим email
            "TestPass123",  # Вводим пароль
            "6",  # Выход из аккаунта
            "1",  # Подтверждение выхода
        ]):
            self.main_menu()

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "1",  # Обновить запись
        "Good",  # Вводим запись
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_create_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем добавление записи"""
        expected_string = ['Текст успешно обновлен!', 'Good']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            user_menu(1)

        result = mock_output.getvalue().strip()  # Сохраняем выведенную строку для сравнения результата теста
        assert result[-4:] in expected_string, (
            f'При добавлении текста возникла ошибка: {result[-4:]} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "2",  # Обновить запись
        "1",  # Выбрать запись
        "Good",  # Вводим запись
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_update_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем добавление записи"""
        expected_string = ['Good', 'У вас еще нет ни одной записи']

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            user_menu(1)

        result = mock_output.getvalue().strip().split()  # Сохраняем выведенную строку для сравнения результата теста
        result = ' '.join(result[-7:])
        assert result in expected_string, (
            f'При добавлении текста возникла ошибка: {result} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "3",  # Удалить запись
        "1",  # Выбираем номер записи
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_delete_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем добавление записи"""
        expected_string = 'У вас еще нет ни одной записи'

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            user_menu(1)

        result = mock_output.getvalue().strip().split()  # Сохраняем выведенную строку для сравнения результата теста
        result = ' '.join(result[-7:])
        assert result == expected_string, (
            f'При добавлении текста возникла ошибка: {result} (ожидалось: {expected_string})'
        )

    @patch("builtins.input", side_effect=[  # Для тестовых функций устанавливаем значения инпутов через patch
        "4",  # Удалить все записи
        "6",  # Выход из аккаунта
        "1",  # Подтверждение выхода
    ])
    def test_delete_all_text(self, mock_input: unittest.mock.MagicMock) -> None:
        """Тестируем функцию удаления записи"""
        expected_list = "У вас еще нет ни одной записи"

        with patch('sys.stdout', new_callable=io.StringIO) as mock_output:
            user_menu(1)

        result = mock_output.getvalue().strip().split()  # Сохраняем выведенную строку для сравнения результата теста
        result = ' '.join(result[-7:])
        assert result in expected_list, (f"При выводе текста возникла ошибка: {result} "
                                                        f"(ожидалось: {expected_list})")


if __name__ == "__main__":
    unittest.main()
