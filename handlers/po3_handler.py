from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import search_spec_doctor
from keyboards.client_kb import spec_client, kb_client
# from main import spec_check
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def polyclinic_3(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000001382')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)