from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.client_kb import choise_client, menu_client, kb_client
#from main import del_entry
from states.states import ClientRequests
from handlers.return_to_main_menu_handler import return_to_main_menu

import logging

logger = logging.getLogger(__name__)

async def cancel_command(message: types.Message):
    await message.answer('Выберите раздел:', reply_markup=choise_client)


async def cancel_doctor_command(message: types.Message, state: FSMContext):
    await message.answer('Введите свой полис ОМС:', reply_markup=menu_client)
    logger.info('ОТМЕНА ЗАПИСИ К ВРАЧУ')
    await state.set_state(ClientRequests.cancel_doctor)

async def cancel_home_command(message: types.Message, state: FSMContext):
    await message.answer('Отменить вызов врача на дом невозможно. Ожидайте звонка оператора.', reply_markup=kb_client)
    await state.clear()
    await return_to_main_menu(message, state)