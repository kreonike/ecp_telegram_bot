import logging
import requests
import authorization
import base_ecp

# Константы
LPU_ID = '2762'
BASE_URL = 'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO'

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def fetch_doctors_by_specialty(specialty_id, session):
    url = f'{BASE_URL}?MedSpecOms_id={specialty_id}&Lpu_id={LPU_ID}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении данных о врачах: {e}')
        raise


def find_doctor_by_surname(doctors_data, surname):
    for doctor in doctors_data.get('data', []):
        if doctor.get('PersonSurName_SurName') == surname:
            return doctor
    return None


def search_doctor(surname):
    logging.info(f'Поиск врача по фамилии: {surname}')

    # Авторизация
    session = authorization.authorization()

    # Получение списка специальностей
    specialty_ids = base_ecp.medspecoms_id.values()

    # Поиск врача по фамилии
    for specialty_id in specialty_ids:
        doctors_data = fetch_doctors_by_specialty(specialty_id, session)
        doctor = find_doctor_by_surname(doctors_data, surname)
        if doctor:
            logging.info(f'Врач найден: {doctor}')
            return doctor

    logging.info('Врач не найден')
    return None
