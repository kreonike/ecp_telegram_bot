import logging
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization
import datetime

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def entry_home(person_id, address_mess, phone_mess, reason_mess):
    print(address_mess)
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()
    # CallProfType_id
    # 1 - терапия, 2 - стоматология

    # HomeVisitCallType
    # 1 простой
    # 2 активный
    # 3 выписка рецепта
    # 4 патронаж
    # 5 вызов узкого специалиста

    KLStreet_id = '393790'
    HomeVisitStatus_id = '1'  # назначен врач
    get_status_address = f'https://ecp.mznn.ru/api/Address?Person_id={person_id}&sess_id={session}'
    result_address = requests.get(get_status_address)
    status_address = result_address.json()
    logging.info(f' person address: {status_address}')

    HomeVisit_House = status_address['data']['1']['Address_House']

    now = datetime.datetime.now()
    time_entry = now.strftime("%d.%m.%Y %H:%m")
    time_default = now.strftime('%d.%m.%Y 12:00')

    if time_default < time_entry:
        print('time_default < time_entry')
        time_entry = now + datetime.timedelta(days=1)
        HomeVisit_setDT = time_entry.strftime("%d.%m.%Y 08:00")
        print(f' if: HomeVisit_setDT')

    else:
        print('time_entry > time_default')
        HomeVisit_setDT = now.strftime("%d.%m.%Y %H:%m")
        print(f' else: HomeVisit_setDT')

    logging.info(f' фактическая дата записи: {HomeVisit_setDT}')

    status_home = f'https://ecp.mznn.ru/api/HomeVisit/HomeVisit?CallProfType_id=1&' \
                  f'Address_Address={address_mess}&KLStreet_id={KLStreet_id}&HomeVisit_House={HomeVisit_House}&HomeVisitCallType_id=1&' \
                  f'HomeVisit_setDT={HomeVisit_setDT}&' \
                  f'HomeVisit_Phone={phone_mess}&HomeVisit_Symptoms={reason_mess}&' \
                  f'HomeVisitStatus_id={HomeVisitStatus_id}&HomeVisitWhoCall_id=1&Person_id={person_id}&sess_id={session}'
    #post запрос
    result_status = requests.post(status_home)
    print(f' rrrr {result_status}')
    status_home = result_status.json()
    print(f' status_home: {status_home}')
    return status_home
