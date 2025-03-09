import logging
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization
from config.config import API_ECP


def entry_status(person_id):
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    ##статус бирки
    status_entry = f'{API_ECP}TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    result_status = requests.get(status_entry)
    status_date = result_status.json()
    # print(status_date)
    return status_date
