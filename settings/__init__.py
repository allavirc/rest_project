from dotenv import load_dotenv # метод который ищет файлы dotenv
from django.core.exceptions import ImproperlyConfigured

import os

load_dotenv()
def get_env_variable(env_variable: str) -> str:
    try:
        return os.getenv(env_variable)  # пытаемся найти виртуалку
    except KeyError:
        raise ImproperlyConfigured( # если такой нет вызываем ошибку
            f'Set {env_variable} enviroment variable'
        )
