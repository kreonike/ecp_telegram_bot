import logging
from config.config import bot_token, login_ecp, password_ecp
import requests

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def authorization():
    login = login_ecp
    password = password_ecp
    link = 'https://ecp.mznn.ru/api/user/login' + '?Login=' + login + '&Password=' + password

    responce = requests.get(link)
    data_session = responce.json()
    session = data_session['sess_id']

    return session


logging.info(f' authorization {authorization()}')
