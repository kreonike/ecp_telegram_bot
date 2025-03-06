from aiogram import types
from keyboards.client_kb import kb_client

async def info_command(message: types.Message):
    await message.answer(
        f' *CТАЦИОНАР ГКБ12*\n'
        f' Нижний Новгородул, ул. Павла Мочалова,8\n'
        f' Секретарь: 273-00-62\n'
        f'\n'
        f' *ПОЛИКЛИНИКА №1*\n'
        f' Нижний Новгород, ул.Васенко,11\n'
        f' регистратура: 280-85-95\n'
        f'\n'
        f' *ПОЛИКЛИНИКА №2*\n'
        f' Нижний Новгород, ул.Свободы, 3\n'
        f' регистратура: 273-03-00\n'
        f'\n'
        f' *ПОЛИКЛИНИКА №3*\n'
        f' Нижний Новгород, ул.Циолковского,9\n'
        f' Регистратура 225-01-87\n'
        f'\n'
        f' *ПОЛИКЛИНИКА №4*\n'
        f' Светлоярская улица, 38А'
        f' регистратура: 271-89-72', reply_markup=kb_client, parse_mode="Markdown")