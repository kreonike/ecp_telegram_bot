from aiogram import types

from keyboards.client_kb import kb_client


async def worker_command(message: types.Message):
    await message.answer(
        f' Стационар ГБК12\n'
        f' круглосуточно\n'
        f'\n'
        f' Поликлиника №1\n'
        f' пн-пт 7:30-19:30\n'
        f' сб-вс 08.30-14.30\n'
        f'\n'
        f' Поликлиника №2\n'
        f' пн-пт 7:30-19:30\n'
        f' \n'
        f' Поликлиника №3\n'
        f' пн-пт 7:30-19:00\n'
        f' сб-вс 08:00-14:00'
        f'\n'
        f' Поликлиника №4\n'
        f' пн-пт 7:30-19:30', reply_markup=kb_client)