import aiohttp
from api import authorization
from config.config import API_ECP

async def entry_status(person_id):
    session = await authorization.authorization()
    url = f'{API_ECP}TimeTableListbyPatient?Person_id={person_id}&sess_id={session}'

    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            response.raise_for_status()
            status_date = await response.json()
            print(f'В entry_status: {status_date}')
            return status_date