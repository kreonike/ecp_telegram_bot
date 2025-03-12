from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import menu_client
from states.states import ClientRequests


async def check_call_command(message: types.Message, state: FSMContext):
    await message.answer('Введите идентификатор: ', reply_markup=menu_client)
    await state.set_state(ClientRequests.checking_home)