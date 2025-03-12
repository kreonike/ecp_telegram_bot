from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import pol_client


async def spec_command(message: types.Message, state: FSMContext):
    await message.reply('Выберите поликлинику', reply_markup=pol_client)
