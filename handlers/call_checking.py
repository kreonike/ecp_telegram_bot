import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import entry_status, search_person, search_polis
from keyboards.client_kb import menu_client, kb_client, ident_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)


async def get_person_polis_call(message: types.Message, state: FSMContext):
    message_polis = message.text

    if message_polis == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif len(message_polis) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса', reply_markup=menu_client)

    elif not message_polis.isdigit():
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов', reply_markup=menu_client)

    else:
        await message.answer('Идёт поиск, подождите ', reply_markup=menu_client)
        polis_data = await search_polis.search_polis(message_polis)  # Используем await
        person = await search_person.search_person(polis_data['data'][0]['Person_id'])  # Используем await
        # global person_id
        person_id = person['data'][0]['Person_id']
        check_entry_data = await entry_status.entry_status(person_id)  # Используем await

        from utils.json_temp_data import save_global_person_id
        save_global_person_id(person_id)

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
        await state.set_state(ClientRequests.call_entry)