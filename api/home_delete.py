import logging
import aiohttp
from api import authorization
from config.config import API_ECP

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def home_delete(homevisit_id):
    print(homevisit_id)
    session = await authorization.authorization()
    url = f'{API_ECP}HomeVisit/HomeVisitCancel?HomeVisit_id={homevisit_id}&sess_id={session}'

    try:
        async with aiohttp.ClientSession() as client:
            async with client.put(url) as response:
                if response.status == 500:
                    print('error')
                    return {'error_code': 6}
                else:
                    status_address = await response.json()
                    print(status_address)
                    return status_address
    except Exception as e:
        print(f'Ошибка: {e}')