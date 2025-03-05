import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization
import datetime

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def home_delete(homevisit_id):
    print(homevisit_id)
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    try:
        get_status_address = f'https://ecp.mznn.ru/api/HomeVisit/HomeVisitCancel?HomeVisit_id=' \
                             f'{homevisit_id}&sess_id={session}'

        result_address = requests.put(get_status_address)
        print(result_address.status_code)
        if result_address.status_code == 500:
            print('error')
            status_address = {'error_code': 6}
            return status_address

        else:
            status_address = result_address.json()
            print(status_address)
            return status_address

    except TypeError:
        print('дата пустое')
