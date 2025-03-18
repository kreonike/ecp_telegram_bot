import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import entry_status, search_person, search_polis
from keyboards.client_kb import menu_client, ident_client, kb_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)

async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text
    if message_polis == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
    elif len(message_polis) != 16 or not message_polis.isdigit():
        await message.reply('Неверный ввод, введите 16 цифр номера полиса без символов и пробелов',
                            reply_markup=menu_client)
    else:
        await message.answer('Идёт поиск, подождите ', reply_markup=menu_client)
        polis_data = search_polis.search_polis(message_polis)
        person = search_person.search_person(polis_data['data'][0]['Person_id'])
        person_id = person['data'][0]['Person_id']
        check_entry_data = entry_status.entry_status(person_id)

        if ('data' in check_entry_data and 'TimeTable' in check_entry_data['data']
                and check_entry_data['data']['TimeTable']):
            time_table_beg_time = check_entry_data['data']['TimeTable'][0]['TimeTable_begTime']
            time_table_id = check_entry_data['data']['TimeTable'][0]['TimeTable_id']
            date_whithout_time = time_table_beg_time.partition(' ')[0]
            await state.update_data(
                person_id=person_id,
                time=time_table_beg_time,
                TimeTableGraf_id=time_table_id
            )
        else:
            await message.reply('Данные о расписании отсутствуют.')
            await state.update_data(person_id=person_id)

        PersonSurName_SurName = person['data'][0]['PersonSurName_SurName']
        PersonFirName_FirName = person['data'][0]['PersonFirName_FirName']
        PersonSecName_SecName = person['data'][0]['PersonSecName_SecName']
        PersonBirthDay_BirthDay = person['data'][0]['PersonBirthDay_BirthDay']
        await message.reply(
            f' Фамилия: {PersonSurName_SurName}\n'
            f' Имя: {PersonFirName_FirName}\n'
            f' Отчество: {PersonSecName_SecName}\n'
            f' Дата рождения: {PersonBirthDay_BirthDay}\n')
        await message.answer('Это Вы ?', reply_markup=ident_client)
        await state.set_state(ClientRequests.entry)