import logging
import aiohttp
from api import authorization
from config.config import API_ECP

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def time_delete(TimeTable_id, TimeTableSource):
    # Авторизация
    session = await authorization.authorization()
    print(f' TimeTableSource: {TimeTableSource}')

    FailCause = 1
    # Удаляем бирку
    delete_time = f'{API_ECP}TimeTable?TimeTable_id={TimeTable_id}&TimeTableSource={TimeTableSource}' \
                  f'&FailCause={FailCause}&sess_id={session}'
    try:
        async with aiohttp.ClientSession() as client:
            async with client.delete(delete_time) as response:
                response.raise_for_status()
                status_delete = await response.json()
                print(f' status_delete::: {status_delete}')
                logging.info(f' БИРКА УДАЛЕНА {status_delete}')
                if status_delete.get('error_code') == 6:
                    print('Бирка не найдена в системе.')
                    error = 6
                    return error
                else:
                    return status_delete
    except aiohttp.ClientError as e:
        logging.error(f'Ошибка при удалении бирки: {e}')
        raise