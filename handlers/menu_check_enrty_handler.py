from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import check_client


async def menu_check_entry_command(message: types.Message, state: FSMContext):
    await message.reply('Запись куда хотите проверить ?', reply_markup=check_client)
