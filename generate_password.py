import random

# Создаем списки символов
letters = "ABCDEFGHIJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz!#$%&*+-=?@^_.23456789"

#
def pass_choice():
    '''Функция генерации пароля'''
    pass_len = random.randint(8, 16)
    password = []
    for _ in range(pass_len):
        password += random.choice(letters)
    return ''.join(password)

