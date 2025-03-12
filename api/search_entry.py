import requests

from api import authorization
from config.config import API_ECP


def search_entry(person_id, TimeTableGraf_id):
    print(f' в функцию search_entry получен {person_id} и {TimeTableGraf_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    ##сама запись post запрос
    search_entry = f'{API_ECP}TimeTableGraf/TimeTableGrafWrite?Person_id={person_id}&' \
                   f'TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'

    result_entry = requests.post(search_entry)
    print(result_entry)
    entry_date = result_entry.json()
    print(f'entry_date в search_entry', entry_date)

    ##статус бирки
    status_entry = f'{API_ECP}TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    result_status = requests.get(status_entry)
    status_date = result_status.json()

    print(status_date)

    return entry_date, status_date
