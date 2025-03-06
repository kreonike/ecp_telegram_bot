import logging
import datetime
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization


def search_date(MedStaffFact_id):
    logging.info(f' search_date - MedStaffFact_id: {MedStaffFact_id}')
    print(f' search_date - MedStaffFact_id: {MedStaffFact_id}')
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()


    now = datetime.datetime.now()

    tomorrow = now + datetime.timedelta(days=1)

    today = now.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    logging.info(f' tomorrow: {tomorrow}')

    result = now + datetime.timedelta(days=14)
    TimeTableGraf_end = result.date()


    search_date = (f' https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafFreeDate?MedStaffFact_id={MedStaffFact_id}'
                   f'&TimeTableGraf_beg={tomorrow}&TimeTableGraf_end={TimeTableGraf_end}&sess_id={session}')

    result_date = requests.get(search_date)
    data_date = result_date.json()
    print(f' data_date::: {data_date}')

    return data_date
