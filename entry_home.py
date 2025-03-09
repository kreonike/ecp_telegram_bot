import datetime
import logging
import requests
import authorization

# константы
CALL_PROF_TYPE_THERAPY = '1'
HOME_VISIT_CALL_TYPE_SIMPLE = '1'
KLSTREET_ID = '393790'
HOME_VISIT_STATUS_ASSIGNED = '1'  # назначен врач

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def get_home_visit_time():
    now = datetime.datetime.now()
    time_entry = now.strftime("%d.%m.%Y %H:%M")
    time_default = now.strftime('%d.%m.%Y 12:00')

    if time_default < time_entry:
        logging.info('time_default < time_entry')
        time_entry = now + datetime.timedelta(days=1)
        home_visit_set_dt = time_entry.strftime("%d.%m.%Y 08:00")
    else:
        logging.info('time_entry > time_default')
        home_visit_set_dt = now.strftime("%d.%m.%Y %H:%M")

    logging.info(f'Фактическая дата записи: {home_visit_set_dt}')
    return home_visit_set_dt


def get_person_address(person_id, session):
    url = f'https://ecp.mznn.ru/api/Address?Person_id={person_id}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        address_data = response.json()
        logging.info(f'Адрес человека: {address_data}')
        return address_data['data']['1']['Address_House']
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении адреса: {e}')
        raise


def create_home_visit(person_id, address_mess, phone_mess, reason_mess, session):
    home_visit_set_dt = get_home_visit_time()
    home_visit_house = get_person_address(person_id, session)

    url = f'https://ecp.mznn.ru/api/HomeVisit/HomeVisit?CallProfType_id={CALL_PROF_TYPE_THERAPY}&' \
          f'Address_Address={address_mess}&KLStreet_id={KLSTREET_ID}&HomeVisit_House={home_visit_house}&' \
          f'HomeVisitCallType_id={HOME_VISIT_CALL_TYPE_SIMPLE}&HomeVisit_setDT={home_visit_set_dt}&' \
          f'HomeVisit_Phone={phone_mess}&HomeVisit_Symptoms={reason_mess}&' \
          f'HomeVisitStatus_id={HOME_VISIT_STATUS_ASSIGNED}&HomeVisitWhoCall_id=1&Person_id={person_id}&sess_id={session}'

    try:
        response = requests.post(url)
        response.raise_for_status()
        result = response.json()
        logging.info(f'Результат создания вызова: {result}')
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при создании вызова: {e}')
        raise


def entry_home(person_id, address_mess, phone_mess, reason_mess):
    logging.info(f'Запрос на вызов на дом для person_id: {person_id}')
    session = authorization.authorization()
    return create_home_visit(person_id, address_mess, phone_mess, reason_mess, session)
