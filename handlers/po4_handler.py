import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import spec_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)

async def polyclinic_4(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000000181')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)
