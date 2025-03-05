import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_entry(person_id, TimeTableGraf_id):
    print(f' в функцию search_entry получен {person_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    ##сама запись post запрос
    search_entry = f'https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafWrite?Person_id={person_id}&' \
                   f'TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'
    result_entry = requests.post(search_entry)
    entry_date = result_entry.json()

    ##статус бирки
    status_entry = f'https://ecp.mznn.ru/api/TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    result_status = requests.get(status_entry)
    status_date = result_status.json()

    # print(status_date)

    return entry_date, status_date
