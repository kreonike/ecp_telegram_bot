import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

import entry_status
import search_person
import search_polis
from keyboards.client_kb import menu_client, kb_client, ident_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)



async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text
    print(f' message_polis: {message_polis}')

    if message_polis == 'вернуться в меню':
        print('@@вернуться в главное меню')
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
        await message.answer('Идёт поиск, подождите ',
                               reply_markup=menu_client)
        polis_data = search_polis.search_polis(message_polis)
        print(f' polis_num из функции: {polis_data}')
        person = search_person.search_person(polis_data['data'][0]['Person_id'])
        person_id = person['data'][0]['Person_id']
        print(f' получена из функции: {person_id}')

        print('=========ПРОВЕРКА=========')
        from utils.json_temp_data import load_postid
        post_id = load_postid()
        print(f' post_id для check: {post_id}')
        print(f' Person_id: {person_id}')
        check_entry_data = entry_status.entry_status(person_id)
        print(check_entry_data)

        data = await state.get_data()
        message_time = data.get('message_time')
        print(message_time)
        date_whithout_time = message_time.partition(' ')[0]

        print(post_id)
        print(check_entry_data)
        print(date_whithout_time)

        from utils.json_temp_data import save_check_error
        #global check_error
        check_error = 0
        save_check_error(check_error)
        for j in check_entry_data['data']['TimeTable']:
            if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[0] == date_whithout_time:
                print('НАЙДЕНО СОВПАДЕНИЕ')
                print('запись к одному и тому же специалисту на один и тот же день запрещена')
                check_error = 6
                save_check_error(check_error)

            else:
                print('совпадений не найдено')

        print(check_error)
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