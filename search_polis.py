import logging
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_polis(polis):
    print(f' получен полис в функцию search_polis: {polis}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    search_polis = f'https://ecp.mznn.ru/api/Polis?Polis_Num={polis}&sess_id={session}'
    result_polis = requests.get(search_polis)
    polis_data = result_polis.json()
    print(f' дата для search_time: {polis_data}')
    # logging.info(f' polis_data {polis_data}')
    return polis_data
