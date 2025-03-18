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

async def entry_status(homevisit_id):
    session = await authorization.authorization()
    url = f'{API_ECP}HomeVisit/HomeVisitById?HomeVisit_id={homevisit_id}&sess_id={session}'

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f'Ошибка при получении статуса вызова: {e}')
        raise