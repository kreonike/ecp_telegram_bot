import aiohttp
from api import authorization
from config.config import API_ECP

async def search_person(person_id):
    print(f' получен person_id в функцию search_person: {person_id}')

    # Авторизация
    session = await authorization.authorization()

    url = f'{API_ECP}Person?Person_id={person_id}&sess_id={session}'

    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            response.raise_for_status()
            person_data = await response.json()
            print(f' дата в person_id: {person_data}')
            return person_data