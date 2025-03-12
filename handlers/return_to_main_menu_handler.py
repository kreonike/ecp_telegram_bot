import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import kb_client

logger = logging.getLogger(__name__)

async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите раздел:', reply_markup=kb_client)



