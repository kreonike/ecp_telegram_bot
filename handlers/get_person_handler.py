import logging
from aiogram import types
from aiogram.fsm.context import FSMContext
from states.states import ClientRequests
from keyboards.client_kb import menu_client, kb_client, ident_client
from api import entry_status, search_person, search_polis
from utils.json_temp_data import load_postid, save_check_error

logger = logging.getLogger(__name__)

async def validate_polis_input(message_polis: str) -> bool:
    if len(message_polis) != 16 or not message_polis.isdigit():
        return False
    return True

async def check_existing_entry(person_id: str, post_id: str, date_without_time: str) -> int:
    check_entry_data = entry_status.entry_status(person_id)
    check_error = 0
    for j in check_entry_data['data']['TimeTable']:
        if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[0] == date_without_time:
            logger.info('Найдено совпадение: запись к одному и тому же специалисту на один и тот же день запрещена')
            check_error = 6
            break
    save_check_error(check_error)
    return check_error

async def get_person_info(person_id: str) -> dict:
    person = search_person.search_person(person_id)
    return {
        'PersonSurName_SurName': person['data'][0]['PersonSurName_SurName'],
        'PersonFirName_FirName': person['data'][0]['PersonFirName_FirName'],
        'PersonSecName_SecName': person['data'][0]['PersonSecName_SecName'],
        'PersonBirthDay_BirthDay': person['data'][0]['PersonBirthDay_BirthDay']
    }

async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text
    logger.info(f'Получен номер полиса: {message_polis}')

    if message_polis == 'вернуться в меню':
        logger.info('Возврат в главное меню')
        await state.set_state(ClientRequests.main_menu)
        await message.reply('Выберите раздел', reply_markup=kb_client)
        await state.clear()
        return

    if not await validate_polis_input(message_polis):
        await message.reply('Неверный ввод. Введите 16 цифр номера полиса без символов и пробелов.', reply_markup=menu_client)
        return

    await message.answer('Идёт поиск, подождите...', reply_markup=menu_client)
    polis_data = search_polis.search_polis(message_polis)
    if not polis_data or not polis_data.get('data'):
        await message.reply('Данные по полису не найдены.', reply_markup=menu_client)
        return

    person_id = polis_data['data'][0]['Person_id']
    logger.info(f'Найден Person_id: {person_id}')

    post_id = load_postid()
    data = await state.get_data()
    message_time = data.get('message_time')
    date_without_time = message_time.partition(' ')[0]

    check_error = await check_existing_entry(person_id, post_id, date_without_time)
    if check_error == 6:
        await message.reply('Запись к одному и тому же специалисту на один и тот же день запрещена.', reply_markup=menu_client)
        return

    await state.update_data(person_id=person_id)
    person_info = await get_person_info(person_id)

    await message.reply(
        f'Фамилия: {person_info["PersonSurName_SurName"]}\n'
        f'Имя: {person_info["PersonFirName_FirName"]}\n'
        f'Отчество: {person_info["PersonSecName_SecName"]}\n'
        f'Дата рождения: {person_info["PersonBirthDay_BirthDay"]}\n'
    )

    await message.answer('Это Вы?', reply_markup=ident_client)
    await state.set_state(ClientRequests.entry)