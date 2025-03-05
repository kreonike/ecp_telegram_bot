import logging
from config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_time2(MedStaffFact_id, TimeTableGraf_begTime):
    print(f' получено значение в search_time1: {MedStaffFact_id}')
    print(f' получено значение в search_time2: {TimeTableGraf_begTime}')
    TimeTableGraf_begTime = TimeTableGraf_begTime.partition(' ')[0]
    print(f' правильный: {TimeTableGraf_begTime}')

    ##авторизация
    authorization.authorization()
    session = authorization.authorization()

    # TODO тип бирки

    search_time = f'http://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={MedStaffFact_id}' \
                  f'&TimeTableGraf_begTime={TimeTableGraf_begTime}&sess_id={session}'

    result_MedStaffFact_id = requests.get(search_time)
    data_MedStaffFact_id = result_MedStaffFact_id.json()
    print(f' дата для search_time: {data_MedStaffFact_id}')

    data_time_dict = {}

    for k in data_MedStaffFact_id['data']:
        TimeTableGraf_begTime = k['TimeTableGraf_begTime']
        data_time_dict[TimeTableGraf_begTime] = k['TimeTableGraf_id']

    print(f' тут финальный словарь из search_time: {data_time_dict}')
    return data_time_dict
