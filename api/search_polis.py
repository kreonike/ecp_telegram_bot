import aiohttp
from api import authorization
from config.config import API_ECP

async def search_polis(polis):
    print(f' получен полис в функцию search_polis: {polis}')

    # Авторизация
    session = await authorization.authorization()

    url = f'{API_ECP}Polis?Polis_Num={polis}&sess_id={session}'

    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            response.raise_for_status()
            polis_data = await response.json()
            print(f' дата для search_time: {polis_data}')
            return polis_data