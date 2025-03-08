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


async def checking_address(message: types.Message, state: FSMContext):
    #global address_mess
    address_mess = message.text
    print(address_mess)
    from utils.json_temp_data import save_address_mess, load_address_mess
    save_address_mess(address_mess)
    await message.answer(
        'Введите свой номер телефона (если Вам не смогут дозвонится, вызор будет анулирован:', reply_markup=menu_client)
    await state.set_state(ClientRequests.phone)