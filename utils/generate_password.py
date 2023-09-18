import random


def generate_password_settings() -> list[str] | str:
    """Функция выбора настроек генерируемого пароля"""
    # Создаем строки
    settings = {
        'digits': ("0123456789", "цифры"),
        'lowercase_letters': ("abcdefghijklmnopqrstuvwxyz", "буквы нижнего регистра"),
        'uppercase_letters': ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "буквы верхнего регистра"),
        'punctuation': ("!#$%&*+-=?@^_.", "символы"),
        'ambiguous': ('il1Lo0O', "неочевидные символы 'il1Lo0O'")
    }

    chars = []
    # Добавляем строки в список в соответствии с выбранными параметрами
    for key, (value, description) in settings.items():
        answer = input(f"Наберите 1, если хотите использовать {description}: ")

        if answer.lower() == '1':
            chars.extend(value)
        elif key == 'ambiguous' and answer.lower() != '1':
            for char in value:
                if char in chars:
                    chars.remove(char)

    # Проверяем содержит ли список строки после параметризации
    if len(chars) == 0:
        print("Вы не выбрали ни один из предложенных вариантов символов")
        return generate_password_settings()
    return generate_password_from_string(chars)


def generate_password_from_string(chars: list) -> str:
    """Генерируем пароль случайной длины из случайных символов списка и возвращаем его"""
    password = [random.choice(chars) for _ in range(random.randint(8, 17))]
    return ''.join(password)

