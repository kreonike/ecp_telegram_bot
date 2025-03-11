import logging
from config.config import BOT_TOKEN, LOGIN_ECP, PASSWORD_ECP
import requests

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def authorization():
    login = LOGIN_ECP
    password = PASSWORD_ECP
    link = 'https://ecp.mznn.ru/api/user/login' + '?Login=' + login + '&Password=' + password

    responce = requests.get(link)
    data_session = responce.json()
    session = data_session['sess_id']

    return session


logging.info(f' authorization {authorization()}')
