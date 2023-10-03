import unittest
import random

from models.users import hash_password
from utils import generate_password


char_set = ['0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+-=?@^_.']


class TestModul(unittest.TestCase):
    def test_pass_choice(self):
        """Тестируем модуль рандомной генерации пароля"""

        letter_list = []

        for letter in char_set:
            letter_list.extend(letter)

        password = generate_password.generate_password_from_string(letter_list)

        for letter in password:
            assert letter in letter_list, f'При выводе текста возникла ошибка'

    def test_hash_password(self):
        """Тестируем модуль хэширования пароля"""

        letter_list = []
        for letter in char_set:
            letter_list.extend(letter)

        password = ''.join([random.choice(letter_list) for _ in range(random.randint(8, 17))])
        password_one = hash_password(password)
        password_two = hash_password(password)
        password_check_one = hash_password(password)
        password_check_two = hash_password(password)

        assert password_one == password_check_one and password_two == password_check_two, \
            f'При сравнении паролей возникла ошибка'
