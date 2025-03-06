from aiogram import types
from keyboards.client_kb import kb_client

async def write_command(message: types.Message):
    await message.answer(version, reply_markup=kb_client)