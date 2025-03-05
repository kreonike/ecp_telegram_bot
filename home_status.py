import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def entry_status_home(HomeVisit_id):
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()


    ##статус вызова на дом
    status_entry_home = f'https://ecp.mznn.ru/api/HomeVisit/HomeVisitById?HomeVisit_id={HomeVisit_id}&sess_id={session}'
    result_status = requests.get(status_entry_home)
    status_date = result_status.json()
    print(status_date)
    return status_date