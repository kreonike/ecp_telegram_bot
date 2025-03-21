import logging
import aiohttp
from api import authorization
from config.config import API_ECP

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def fetch_available_times(med_staff_fact_id, beg_time, session):
    url = f'{API_ECP}TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={med_staff_fact_id}&TimeTableGraf_begTime={beg_time}&sess_id={session}'
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f'Ошибка при получении доступного времени: {e}')
        raise

def process_time_data(data):
    return {item['TimeTableGraf_begTime']: item['TimeTableGraf_id'] for item in data.get('data', [])}

async def search_time2(med_staff_fact_id, time_table_graf_beg_time):
    logging.info(
        f'Поиск доступного времени для MedStaffFact_id: {med_staff_fact_id}, '
        f'TimeTableGraf_begTime: {time_table_graf_beg_time}')

    # Очистка времени от лишних данных
    time_table_graf_beg_time = time_table_graf_beg_time.partition(' ')[0]
    logging.info(f'Очищенное время: {time_table_graf_beg_time}')

    # Авторизация
    session = await authorization.authorization()

    # Получение данных о доступном времени
    time_data = await fetch_available_times(med_staff_fact_id, time_table_graf_beg_time, session)
    logging.info(f'Данные о доступном времени: {time_data}')

    # Обработка данных
    data_time_dict = process_time_data(time_data)
    logging.info(f'Финальный словарь: {data_time_dict}')

    return data_time_dict