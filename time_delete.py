import logging
from config.config import bot_token, login_ecp, password_ecp
import requests
import authorization


def time_delete(TimeTable_id, TimeTableSource):
    ##авторизация
    authorization.authorization()
    session = authorization.authorization()
    print(f' TimeTableSource: {TimeTableSource}')
    # logging.info(f' TimeTableSource {TimeTableSource}')
    FailCause = 1
    ##удаляем бирку
    delete_time = f'https://ecp.mznn.ru/api/TimeTable?TimeTable_id={TimeTable_id}&TimeTableSource={TimeTableSource}' \
                  f'&FailCause={FailCause}&sess_id={session}'
    result_detele = requests.delete(delete_time)
    status_delete = result_detele.json()
    print(f' status_delete::: {status_delete}')
    logging.info(f' БИРКА УДАЛЕНА {status_delete}')
    if status_delete['error_code'] == 6:  # or status_delete['error_code'] != 0:
        print('Бирка не найдена в системе.')
        error = 6
        return error
    else:
        return status_delete
