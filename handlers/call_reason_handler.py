from aiogram import types
from aiogram.fsm.context import FSMContext

import entry_status
import search_person
import search_polis
from keyboards.client_kb import menu_client, kb_client, ident_client
from states.states import ClientRequests
import search_time2
import logging

logger = logging.getLogger(__name__)


async def checking_reason(message: types.Message, state: FSMContext):
    #global reason_mess



    reason_mess = message.text
    print(reason_mess)
    from utils.json_temp_data import save_global_person_id, load_global_person_id, load_phone_mess, load_address_mess, save_global_spec_dict_final, save_reason_mess
    person_id = load_global_person_id()
    address_mess = load_address_mess()
    phone_mess = load_phone_mess()
    save_reason_mess(reason_mess)

    print(person_id)
    await message.answer(f' Вы ввели:\n'
                         f' Адресс: {address_mess}\n'
                         f' Телефон: {phone_mess}\n'
                         f' Причина вызова: {reason_mess}\n'
                         f'\n'
                         f' Всё верно ? Отменить запись можно будет только через оператора, '
                         f'если Вы записываетесь после 12:00, то вызов врача будет назначен'
                         f' на завтра', reply_markup=ident_client)
    await state.set_state(ClientRequests.call_entry_question)