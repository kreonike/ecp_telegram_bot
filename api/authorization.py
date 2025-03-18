import logging
import aiohttp
from config.config import LOGIN_ECP, PASSWORD_ECP

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def authorization():
    login = LOGIN_ECP
    password = PASSWORD_ECP
    link = f'https://ecp.mznn.ru/api/user/login?Login={login}&Password={password}'

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            data_session = await response.json()
            session_id = data_session['sess_id']
            logging.info(f'Authorization successful, session ID: {session_id}')
            return session_id