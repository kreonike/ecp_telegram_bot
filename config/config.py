import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LOGIN_ECP = os.getenv('LOGIN_ECP')
PASSWORD_ECP = os.getenv('PASSWORD_ECP')

API_ECP = 'https://ecp.mznn.ru/api/'
