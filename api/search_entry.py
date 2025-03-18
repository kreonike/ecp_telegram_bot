import aiohttp
from api import authorization
from config.config import API_ECP

async def search_entry(person_id, TimeTableGraf_id):
    print(f' в функцию search_entry получен {person_id} и {TimeTableGraf_id}')

    # Авторизация
    session = await authorization.authorization()

    # Сама запись POST запрос
    url = f'{API_ECP}TimeTableGraf/TimeTableGrafWrite?Person_id={person_id}&TimeTableGraf_id={TimeTableGraf_id}&sess_id={session}'

    async with aiohttp.ClientSession() as client:
        async with client.post(url) as response:
            response.raise_for_status()
            entry_date = await response.json()
            print(f'entry_date в search_entry: {entry_date}')

    # Статус бирки
    status_url = f'{API_ECP}TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'
    async with aiohttp.ClientSession() as client:
        async with client.get(status_url) as response:
            response.raise_for_status()
            status_date = await response.json()
            print(f'status_date в search_entry: {status_date}')

    return entry_date, status_date