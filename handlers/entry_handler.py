import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import search_entry
from keyboards.client_kb import kb_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)

async def entry_person(message: types.Message, state: FSMContext):
    message_entry = message.text
    logger.info(f"Получен ввод: {message_entry}")

    if message_entry == 'вернуться в меню':
        logger.info("Возврат в главное меню")
        await state.set_state(ClientRequests.main_menu)
        await message.reply('Выберите раздел', reply_markup=kb_client)
        await state.clear()
        return

    elif message_entry == 'ДА':
        # Получаем данные из состояния
        data = await state.get_data()
        time = data.get('time')
        TimeTableGraf_id = data.get('TimeTableGraf_id')
        person_id = data.get('person_id')

        # Проверка наличия всех необходимых данных
        if not all([time, TimeTableGraf_id, person_id]):
            logger.error(f"Неполные данные в состоянии: time={time}, TimeTableGraf_id={TimeTableGraf_id}, person_id={person_id}")
            await message.reply('Ошибка: неполные данные для записи.')
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Выберите раздел', reply_markup=kb_client)
            await state.clear()
            return

        logger.info(f"Данные для записи: time={time}, TimeTableGraf_id={TimeTableGraf_id}, person_id={person_id}")

        # Проверка дублирования записи (check_error)
        from utils.json_temp_data import load_check_error
        check_error = load_check_error()
        logger.info(f"check_error={check_error}")

        if check_error == 6:
            await message.reply('Запись к одному и тому же специалисту на один и тот же день запрещена.')
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Выберите раздел', reply_markup=kb_client)
            await state.clear()
            return

        elif check_error == 0:
            # Выполняем запись
            entry_data = search_entry.search_entry(person_id, TimeTableGraf_id)
            logger.info(f"Результат search_entry: {entry_data}")

            # Проверка результата API
            if isinstance(entry_data, dict) and 'error_code' in entry_data and entry_data['error_code'] != 0:
                logger.error(f"Ошибка API: {entry_data.get('error_msg', 'Неизвестная ошибка')}")
                await message.reply(f"Ошибка при записи: {entry_data.get('error_msg', 'Попробуйте позже.')}")
                await state.set_state(ClientRequests.main_menu)
                await message.reply('Выберите раздел', reply_markup=kb_client)
                await state.clear()
                return

            # Обработка успешного результата
            try:
                status_date = entry_data[1]  # Предполагаем, что entry_data[1] - это status_date
                if ('data' in status_date and 'TimeTable' in status_date['data']
                        and status_date['data']['TimeTable']):
                    response_lines = []
                    for entry in status_date['data']['TimeTable']:
                        post_name = entry['Post_name']
                        beg_time = entry['TimeTable_begTime']
                        response_lines.append(f"{post_name} на: {beg_time}")
                    response = ("ВЫ ЗАПИСАНЫ к:\n" + "\n".join(response_lines) +
                                "\nПриходите к назначенному времени сразу к врачу,\nв регистратуру идти не нужно")
                    await message.answer(response, reply_markup=kb_client)
                else:
                    raise KeyError("Отсутствуют данные о записи в ответе API")
            except (IndexError, KeyError, TypeError) as e:
                logger.error(f"Ошибка обработки entry_data: {e}, данные: {entry_data}")
                await message.answer("Данных по записи не найдено.", reply_markup=kb_client)

            await state.set_state(ClientRequests.main_menu)
            await state.clear()

    elif message_entry == 'НЕТ':
        logger.info("Пользователь выбрал 'НЕТ'")
        await state.set_state(ClientRequests.main_menu)
        await message.answer('Выберите раздел', reply_markup=kb_client)
        await state.clear()

    else:
        # Обработка некорректного ввода
        await message.reply('Повторите ввод: выберите "ДА" или "НЕТ" нажатием на кнопки или словами')
