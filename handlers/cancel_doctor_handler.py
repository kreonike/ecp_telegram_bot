from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import entry_status
import search_person
import search_polis
import search_spec_doctor
from keyboards.client_kb import spec_client, kb_client, menu_client
# from main import spec_check
from states.states import ClientRequests
from handlers.return_to_main_menu_handler import return_to_main_menu
import logging

logger = logging.getLogger(__name__)

async def checking_entry(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск, подождите...', reply_markup=menu_client)
    mess = message.text
    logger.info(f"Получено сообщение: {mess}")

    # Обработка команды "вернуться в меню"
    if mess == 'вернуться в меню':
        logger.info("Пользователь вернулся в главное меню")
        await return_to_main_menu(message, state)
        return

    # Проверка, что введены только цифры
    if not mess.isdigit():
        await message.reply('Неверный ввод. Вводите только цифры, без символов и пробелов.')
        return

    # Проверка длины номера полиса
    if len(mess) != 16:
        await message.reply('Неверный ввод. Номер полиса должен содержать 16 цифр.')
        return

    # Поиск данных по полису
    logger.info("Поиск данных по полису...")
    polis_data = search_polis.search_polis(mess)

    if not polis_data['data']:
        logger.warning("Полис не найден")
        await message.reply('Неверный ввод. Такого полиса не существует.')
        return

    # Получение данных о человеке
    person_id = polis_data['data'][0]['Person_id']
    person_data = search_person.search_person(person_id)

    if not person_data['data']:
        logger.error("Данные о человеке не найдены")
        await message.reply('Ошибка: данные о человеке не найдены.')
        return

    # Получение данных о записях
    entry_data = entry_status.entry_status(person_id)
    await state.update_data(entry_data_delete=entry_data)

    if not entry_data['data']['TimeTable']:
        logger.info("Записей на приём не найдено")
        await message.answer('ЗАПИСЕЙ НА ПРИЁМ НЕ НАЙДЕНО.')
        await return_to_main_menu(message, state)
        return

    # Отображение информации о записях
    for key in entry_data['data']['TimeTable']:
        name = key['Post_name']
        time = key['TimeTable_begTime']
        id = key['TimeTable_id']
        await message.answer(
            f'Вы записаны к: {name}\n'
            f'На время: {time}\n'
            f'ID бирки: `{id}`',
            parse_mode="Markdown"
        )

    # Запрос ID бирки для отмены
    await message.answer('Если желаете отменить запись, введите ID бирки:', reply_markup=menu_client)
    await state.set_state(ClientRequests.entry_delete)