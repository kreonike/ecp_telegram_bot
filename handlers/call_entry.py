import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import menu_client, kb_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)


async def get_person(message: types.Message, state: FSMContext):
    message_entry = message.text
    from utils.json_temp_data import load_global_person_id
    person_id = load_global_person_id()
    print(person_id)

    if message_entry == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif message_entry == 'ДА':
        await state.set_state(ClientRequests.call_address)
        await message.answer('По какому адресу хотите вызвать врача ? (улица, дом, квартира):', reply_markup=menu_client)

    elif message_entry == 'НЕТ':
        await state.set_state(ClientRequests.main_menu)
        await message.answer('выберите раздел', reply_markup=kb_client)
        await state.clear()

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')