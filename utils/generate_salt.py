import binascii
import os
from decouple import config


def generate_and_save_salt():
    """Генерирует соль и записывает ее в .env"""
    salt = config('SECRET_SALT', default=None)
    if salt is None:
        salt_bytes = os.urandom(16)
        salt = binascii.hexlify(salt_bytes).decode('utf-8')
        with open('../.env', 'a') as env_file:
            env_file.write(f'SECRET_SALT={salt}\n')
    return salt


if __name__ == "__main__":
    generate_and_save_salt()
