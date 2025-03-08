import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import menu_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)


async def checking_phone(message: types.Message, state: FSMContext):
    #global phone_mess
    phone_mess = message.text
    from utils.json_temp_data import save_phone_mess
    save_phone_mess(phone_mess)
    await message.answer('Введите причину вызова,  например (температура, давление):', reply_markup=menu_client)
    await state.set_state(ClientRequests.reason)