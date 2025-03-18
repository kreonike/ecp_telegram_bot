import logging
import aiohttp
from api import authorization

# Константы
LPU_ID = '2762'
BASE_URL = 'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO'
STOMAT_SPECIALTIES = ['520101000000160', '520101000000197', '520101000000165']

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def fetch_doctors_by_specialty(specialty_id, pol, session):
    url = f'{BASE_URL}?MedSpecOms_id={specialty_id}&Lpu_id={LPU_ID}&LpuBuilding_id={pol}&sess_id={session}'
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f'Ошибка при получении данных о врачах: {e}')
        raise

async def combine_doctors_data(specialties, pol, session):
    combined_data = []
    for specialty_id in specialties:
        data = await fetch_doctors_by_specialty(specialty_id, pol, session)
        combined_data.extend(data.get('data', []))
    return combined_data

async def search_spec_doctor(base_ecp_spec, pol):
    logging.info(f'Поиск врачей по специальности: {base_ecp_spec}, корпус: {pol}')

    # Авторизация
    session = await authorization.authorization()

    # Обработка специальностей
    if base_ecp_spec == 520101000000160:
        logging.info('Обработка стоматологических специальностей')
        doctors_data = await combine_doctors_data(STOMAT_SPECIALTIES, pol, session)
    else:
        logging.info(f'Обработка специальности: {base_ecp_spec}')
        doctors_data = (await fetch_doctors_by_specialty(base_ecp_spec, pol, session)).get('data', [])

    logging.info(f'Найдено врачей: {len(doctors_data)}')
    return doctors_data