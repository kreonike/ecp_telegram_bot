import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_person(person_id):
    print(f' получен person_id в функцию search_person: {person_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    search_person = f'https://ecp.mznn.ru/api/Person?Person_id={person_id}&sess_id={session}'
    result_person = requests.get(search_person)
    person_data = result_person.json()
    print(f' дата в person_id: {person_data}')
    # g.info(f' person_data {person_data}')
    return person_data
