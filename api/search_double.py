import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

async def search_double(post_id, check_entry_data, date_whithout_time):
    for j in check_entry_data['data']['TimeTable']:
        if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[0] == date_whithout_time:
            logger.info('НАЙДЕНО СОВПАДЕНИЕ')
            logger.info('запись к одному и тому же специалисту на один и тот же день запрещена')
            error = 6
            return error
        else:
            logger.info('совпадений не найдено')
            error = 0
            return error