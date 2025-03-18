import datetime
import logging
import aiohttp
from api import authorization
from config.config import API_ECP

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def get_date_range():
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    end_date = now + datetime.timedelta(days=14)

    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    logging.info(f'Дата начала поиска: {tomorrow_str}, Дата окончания поиска: {end_date_str}')
    return tomorrow_str, end_date_str

async def fetch_available_dates(med_staff_fact_id, session):
    tomorrow_str, end_date_str = await get_date_range()

    url = (f'{API_ECP}TimeTableGraf/TimeTableGrafFreeDate?'
           f'MedStaffFact_id={med_staff_fact_id}&'
           f'TimeTableGraf_beg={tomorrow_str}&'
           f'TimeTableGraf_end={end_date_str}&'
           f'sess_id={session}')

    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                logging.info(f'Данные о доступных датах: {data}')
                return data
    except aiohttp.ClientError as e:
        logging.error(f'Ошибка при получении данных о доступных датах: {e}')
        raise

async def search_date(med_staff_fact_id):
    logging.info(f'Поиск доступных дат для MedStaffFact_id: {med_staff_fact_id}')

    # Авторизация
    session = await authorization.authorization()

    # Получение доступных дат
    try:
        data_date = await fetch_available_dates(med_staff_fact_id, session)
        return data_date
    except Exception as e:
        logging.error(f'Ошибка в функции search_date: {e}')
        raise