import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import time_delete
from handlers.return_to_main_menu_handler import return_to_main_menu
from keyboards.client_kb import kb_client, menu_client

logger = logging.getLogger(__name__)


async def del_entry(message_delete, entry_data):
    print(message_delete)
    print(entry_data)
    del_error = ''
    for key in entry_data['data']['TimeTable']:
        if key['TimeTable_id'] == message_delete:
            print('TimeTable_id = message_delete')
            TimeTableSource = 'Graf'
            status_del = await time_delete.time_delete(message_delete, TimeTableSource)  # Используем await
            print(f' status_del: ! {status_del}')

            if status_del.get('data') == []:  # Используем .get() для безопасного доступа
                print('done')
                del_error = '0'
                return del_error

        elif key['TimeTable_id'] != message_delete:
            print(f' error {del_error}')
            del_error = '6'
            print(del_error)
            return del_error


async def get_delete(message: types.Message, state: FSMContext):
    message_delete = message.text
    logger.info(f"Получено сообщение для отмены: {message_delete}")

    # Обработка команды "вернуться в меню"
    if message_delete == 'вернуться в меню':
        logger.info("Пользователь вернулся в главное меню")
        await return_to_main_menu(message, state)
        return

    # Проверка, что введены только цифры
    if not message_delete.isdigit():
        await message.reply('Неверный ввод. Вводите только цифры, без символов и пробелов.', reply_markup=menu_client)
        return

    # Отмена записи
    data = await state.get_data()
    entry_data = data.get('entry_data_delete')
    del_status = await del_entry(message_delete, entry_data)  # Используем await
    logger.info(f"Результат отмены записи: {del_status}")

    if del_status == '0':
        await message.answer('БИРКА УДАЛЕНА.', reply_markup=kb_client)
        await return_to_main_menu(message, state)
    elif del_status == '6':
        await message.answer('Бирка не найдена. Повторите ввод.', reply_markup=menu_client)
    else:
        await message.answer('Неверный ID бирки. Повторите попытку.', reply_markup=menu_client)