import logging
import requests
from aiogram import Bot
from tqdm import tqdm
from api import authorization
from config.config import API_ECP
import asyncio

# Константы
ALLOWED_TIMETABLE_TYPES = {'1', '4', '10', '11'}
####
###
#https://ecp.mznn.ru/api/Refbook?Refbook_Code=dbo.TimeTableType
# 1: "Обычная"
# 2: "Резервная"
# 3: "Платная"
# 4: "ЦЗ"
# 5: "По направлению"
# 6: "Экстренная"
# 7: "Койки ЧС"
# 8: "Для врачей своей МО"
# 9: "Запись через инфомат"
# 10: "Через регистратуру МО"
# 11: "Для интернета"
# 12: "Живая очередь"
# 13: "Видеосвязь"
# 14: "Групповой прием"
# 15:
# 16:
# 17:
# 18: "Диспансерный учёт"
# 19: "ТМК"
###
####

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

async def fetch_available_times(med_staff_fact_id, beg_time, session):
    url = f'{API_ECP}TimeTableGraf/TimeTableGrafFreeTime?MedStaffFact_id={med_staff_fact_id}&TimeTableGraf_begTime={beg_time}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении доступного времени: {e}')
        raise

async def fetch_timetable_details(time_table_graf_id, session):
    url = f'{API_ECP}TimeTableGraf/TimeTableGrafById?TimeTableGraf_id={time_table_graf_id}&sess_id={session}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Ошибка при получении деталей расписания: {e}')
        raise

def filter_allowed_timetable_types(data):
    return [item for item in data if item.get('TimeTableType_id') in ALLOWED_TIMETABLE_TYPES]

async def search_time(med_staff_fact_id, data_date_dict, bot: Bot, message):
    logging.info(f'Поиск доступного времени для MedStaffFact_id: {med_staff_fact_id}')

    # Авторизация
    session = authorization.authorization()

    # Извлечение времени начала
    beg_time_list = [key['TimeTableGraf_begTime'] for key in data_date_dict.get('data', [])]
    logging.info(f'Список времени начала: {beg_time_list}')
    logging.info(f"Количество элементов в beg_time_list: {len(beg_time_list)}")

    # Поиск доступного времени
    data_time_list = []
    total_tasks = len(beg_time_list)

    # Отправляем начальное сообщение
    progress_message = await bot.send_message(
        message.chat.id,
        "Идёт поиск сводных дат для записи, это может занять много времени, пожалуйста ожидайте.. (0%)"
    )

    # Используем tqdm для отслеживания прогресса
    for i, beg_time in enumerate(tqdm(beg_time_list, desc="Поиск доступного времени", unit="запрос")):
        time_data = await fetch_available_times(med_staff_fact_id, beg_time, session)
        for item in time_data.get('data', []):
            timetable_details = await fetch_timetable_details(item['TimeTableGraf_id'], session)
            filtered_data = filter_allowed_timetable_types(timetable_details.get('data', []))
            data_time_list.extend(filtered_data)

        # Вычисляем процент выполнения
        progress_percent = int(((i + 1) / total_tasks) * 100)

        # Обновляем сообщение на каждой итерации
        logging.info(f"Обновление прогресса: {progress_percent}%")
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=progress_message.message_id,
            text=f"Идёт поиск сводных дат для записи, это может занять много времени, пожалуйста ожидайте.. ({progress_percent}%)"
        )
        await asyncio.sleep(1)  # Задержка 1 секунда для соответствия лимитам Telegram

    logging.info(f'Найдено доступных времен: {len(data_time_list)}')
    return data_time_list