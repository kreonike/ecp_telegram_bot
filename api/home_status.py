import requests
from api import authorization
from config.config import API_ECP


def entry_status_home(HomeVisit_id):
    # авторизация
    authorization.authorization()
    session = authorization.authorization()


    # статус вызова на дом
    status_entry_home = f'{API_ECP}HomeVisit/HomeVisitById?HomeVisit_id={HomeVisit_id}&sess_id={session}'
    result_status = requests.get(status_entry_home)
    status_date = result_status.json()
    print(status_date)
    return status_date
