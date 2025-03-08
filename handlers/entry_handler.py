from aiogram import types
from aiogram.fsm.context import FSMContext

import search_entry
from keyboards.client_kb import kb_client, menu_client
from states.states import ClientRequests

import logging

logger = logging.getLogger(__name__)

async def entry_person(message: types.Message, state: FSMContext):
    message_entry = message.text
    print(message_entry)

    if message_entry == 'вернуться в меню':
        print('вернуться %%%%%%% в главное меню')
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()


    elif message_entry == 'ДА':
        from utils.json_temp_data import save_check_error, load_check_error
        check_error = load_check_error()
        print(f' check_error', check_error)
        if check_error == 6:

            await state.set_state(ClientRequests.main_menu)
            await message.reply(
                'запись к одному и тому же специалисту на один и тот же день запрещена')
            await state.set_state(ClientRequests.main_menu)
            await message.reply('выберите раздел', reply_markup=kb_client)
            spec_dict_final = {}
            await state.clear()

        elif check_error == 0:
            print('0000')
            data = await state.get_data()
            time = data.get('time')
            TimeTableGraf_id = data.get('TimeTableGraf_id')
            person_id = data.get('person_id')

            print(f' message_time: {time}')
            print(f' TimeTableGraf_id: {TimeTableGraf_id}')
            print(f' person_id: {person_id}')

            entry_data = search_entry.search_entry(person_id, TimeTableGraf_id)
            print(f' entry_data: {entry_data}')
            logging.info(f' ЗАПИСЬ {entry_data}')
            await message.answer(
                                   f" ВЫ ЗАПИСАНЫ к:\n"
                                   f" {entry_data[1]['data']['TimeTable'][0]['Post_name']}"
                                   f" на: {entry_data[1]['data']['TimeTable'][0]['TimeTable_begTime']}\n"
                                   f" приходите к назначенному времени сразу к врачу,\n в регистратуру идти не нужно",
                                   reply_markup=kb_client)

            await state.set_state(ClientRequests.main_menu)
            spec_dict_final = {}
            await state.clear()


        else:
            await message.answer(
                                   f' возникла какая-то ошибка, сообщите о пробеме @rapot'
                                   f' или попытайтесь позже', reply_markup=menu_client)

    elif message_entry == 'НЕТ':

        await state.set_state(ClientRequests.main_menu)
        await message.answer('выберите раздел',
                               reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()
        # await ClientRequests.next()


    elif message_entry != 'ДА' or message_entry != 'НЕТ' or message_entry != 'вернуться в меню':
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')