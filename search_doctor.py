import logging
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization
import base_ecp

lpu_id = 'Lpu_id=2762'
def search_doctor(d_final):
    fast_id = base_ecp.medspecoms_id.values()
    print(f' передано значение: {d_final}')
    # logging.info(f' d_final {d_final}')
    ###мне вот эта конструкция не нравится

    id_fast = 1

    ###############################

    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    for i in fast_id:
        search_fast_id = f'http://ecp.mznn.ru/api/MedStaffFact/MedStaffFactByMO?MedSpecOms_id={i}&' \
                         f'{lpu_id}&sess_id={session}'

        result_fast_id = requests.get(search_fast_id)
        data_fast_id = result_fast_id.json()

        for k in data_fast_id['data']:
            if d_final == k['PersonSurName_SurName']:
                id_fast = k
            else:
                pass
    return id_fast
