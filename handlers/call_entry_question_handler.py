from aiogram import types
from aiogram.fsm.context import FSMContext

from api import entry_home
from keyboards.client_kb import kb_client
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)


async def get_person_question(message: types.Message, state: FSMContext):
    message_entry = message.text

    from utils.json_temp_data import load_global_person_id, load_phone_mess, load_address_mess, load_reason_mess
    person_id = load_global_person_id()
    address_mess = load_address_mess()
    phone_mess = load_phone_mess()
    reason_mess = load_reason_mess()

    if message_entry == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif message_entry == 'ДА':
        await message.answer('Выполняется запрос, ожидайте', reply_markup=kb_client)
        result_call_entry = await entry_home.entry_home(person_id, address_mess, phone_mess, reason_mess)  # Используем await
        logging.info(f' result_call_entry: {result_call_entry}')

        if result_call_entry.get('error_code') == 6:  # Используем .get() для безопасного доступа
            await state.set_state(ClientRequests.main_menu)
            await message.answer('У вас уже есть необслуженная запись', reply_markup=kb_client)
            await message.answer('выберите раздел', reply_markup=kb_client)
            await state.clear()

        else:
            HomeVisit_id = result_call_entry['data']['HomeVisit_id']
            await state.set_state(ClientRequests.main_menu)
            HomeVisit_setDT = result_call_entry['data']['HomeVisit_setDT']
            await message.answer(f'Вы успешно записаны, дата записи: {HomeVisit_setDT}\n')
            await message.answer(f" идентификатор: `{HomeVisit_id}`", parse_mode="Markdown")
            await state.clear()

    elif message_entry == 'НЕТ':
        await state.set_state(ClientRequests.main_menu)
        await message.answer('выберите раздел', reply_markup=kb_client)
        await state.clear()

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')