import unittest
import random

from utils import generate_password
from utils import menu

settings = ['0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+-=?@^_.']


class TestModuls(unittest.TestCase):
    def test_pass_choice(self):
        """Тестируем модуль рандомной генерации пароля"""

        letter_list = []

        for letter in settings:
            letter_list.extend(letter)

        password = generate_password.pass_choice(letter_list)

        for letter in password:
            assert letter in letter_list, f'При выводе текста возникла ошибка'

    def test_hash_password(self):
        """Тестируем модуль хэширования пароля"""

        letter_list = []
        for letter in settings:
            letter_list.extend(letter)

        password = ''.join([random.choice(letter_list) for _ in range(random.randint(8, 17))])
        password_one, salt_one = menu.hash_password(password)
        password_two, salt_two = menu.hash_password(password)
        password_check_one, _ = menu.hash_password(password, salt_one)
        password_check_two, _ = menu.hash_password(password, salt_two)

        assert password_one != password_two and password_check_one != password_check_two, \
            f'При сравнении паролей возникла ошибка'
        assert password_one == password_check_one and password_two == password_check_two, \
            f'При сравнении паролей возникла ошибка'
