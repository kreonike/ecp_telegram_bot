import os

from dotenv import load_dotenv

env_file = '.env.template'

if not os.path.exists(env_file):
    exit(f"Переменные окружения не загружены т.к отсутствует файл {env_file}")
else:
    load_dotenv(dotenv_path=env_file)

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOGIN_ECP = os.getenv('LOGIN_ECP')
PASSWORD_ECP = os.getenv('PASSWORD_ECP')

API_ECP = 'https://ecp.mznn.ru/api/'
