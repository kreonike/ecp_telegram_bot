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


async def checking_phone(message: types.Message, state: FSMContext):
    #global phone_mess
    phone_mess = message.text
    from config.config import save_phone_mess
    save_phone_mess(phone_mess)
    await message.answer('Введите причину вызова,  например (температура, давление):', reply_markup=menu_client)
    await state.set_state(ClientRequests.reason)