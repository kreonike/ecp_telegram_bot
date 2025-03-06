from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.client_kb import menu_client, ident_client, kb_client
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text
    if message_polis == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()
    elif len(message_polis) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса',
                            reply_markup=menu_client)
    elif message_polis.isdigit() == False:
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов',
                            reply_markup=menu_client)
    elif message_polis.isdigit() == True:
        await bot.send_message(message.from_user.id, 'Идёт поиск, подождите ',
                               reply_markup=menu_client)
        polis_data = search_polis.search_polis(message_polis)
        person = search_person.search_person(polis_data['data'][0]['Person_id'])
        person_id = person['data'][0]['Person_id']
        check_entry_data = entry_status.entry_status(person_id)
        data = await state.get_data()
        message_time = data.get('message_time')
        date_whithout_time = message_time.partition(' ')[0]
        global check_error
        check_error = 0
        for j in check_entry_data['data']['TimeTable']:
            if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[0] == date_whithout_time:
                check_error = 6
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
        await bot.send_message(message.from_user.id, 'Это Вы ?', reply_markup=ident_client)
        await state.set_state(ClientRequests.entry)