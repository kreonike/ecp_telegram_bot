from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.return_to_main_menu_handler import return_to_main_menu
from keyboards.client_kb import menu_client, pol_client, check_client
from states.states import ClientRequests


async def menu_check_entry_command(message: types.Message, state: FSMContext):
    await message.reply('Запись куда хотите проверить ?', reply_markup=check_client)
