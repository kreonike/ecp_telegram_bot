import logging
import requests
from api import authorization

# Константы
LPU_ID = '2762'
BASE_URL = 'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO'
STOMAT_SPECIALTIES = ['520101000000160', '520101000000197', '520101000000165']

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def fetch_doctors_by_specialty(specialty_id, pol, session):
    url = f'{BASE_URL}?MedSpecOms_id={specialty_id}&Lpu_id={LPU_ID}&LpuBuilding_id={pol}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении данных о врачах: {e}')
        raise


def combine_doctors_data(specialties, pol, session):
    combined_data = []
    for specialty_id in specialties:
        data = fetch_doctors_by_specialty(specialty_id, pol, session)
        combined_data.extend(data.get('data', []))
    return combined_data


def search_spec_doctor(base_ecp_spec, pol):
    logging.info(f'Поиск врачей по специальности: {base_ecp_spec}, корпус: {pol}')

    # Авторизация
    session = authorization.authorization()

    # Обработка специальностей
    if base_ecp_spec == 520101000000160:
        logging.info('Обработка стоматологических специальностей')
        doctors_data = combine_doctors_data(STOMAT_SPECIALTIES, pol, session)
    else:
        logging.info(f'Обработка специальности: {base_ecp_spec}')
        doctors_data = fetch_doctors_by_specialty(base_ecp_spec, pol, session).get('data', [])

    logging.info(f'Найдено врачей: {len(doctors_data)}')
    return doctors_data