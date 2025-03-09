import logging
import requests
import authorization

# Константы
BASE_URL = 'http://ecp.mznn.ru/api/TimeTableGraf'
ALLOWED_TIMETABLE_TYPES = {'1', '4', '10', '11'}

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def fetch_available_times(med_staff_fact_id, beg_time, session):
    url = f'{BASE_URL}/TimeTableGrafFreeTime?MedStaffFact_id={med_staff_fact_id}&TimeTableGraf_begTime={beg_time}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении доступного времени: {e}')
        raise


def fetch_timetable_details(time_table_graf_id, session):
    url = f'{BASE_URL}/TimeTableGrafById?TimeTableGraf_id={time_table_graf_id}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении деталей расписания: {e}')
        raise


def filter_allowed_timetable_types(data):
    return [item for item in data if item.get('TimeTableType_id') in ALLOWED_TIMETABLE_TYPES]


def search_time(med_staff_fact_id, data_date_dict):
    logging.info(f'Поиск доступного времени для MedStaffFact_id: {med_staff_fact_id}')

    # Авторизация
    session = authorization.authorization()

    # Извлечение времени начала
    beg_time_list = [key['TimeTableGraf_begTime'] for key in data_date_dict.get('data', [])]
    logging.info(f'Список времени начала: {beg_time_list}')

    # Поиск доступного времени
    data_time_list = []
    for beg_time in beg_time_list:
        time_data = fetch_available_times(med_staff_fact_id, beg_time, session)
        for item in time_data.get('data', []):
            timetable_details = fetch_timetable_details(item['TimeTableGraf_id'], session)
            filtered_data = filter_allowed_timetable_types(timetable_details.get('data', []))
            data_time_list.extend(filtered_data)

    logging.info(f'Найдено доступных времен: {len(data_time_list)}')
    return data_time_list