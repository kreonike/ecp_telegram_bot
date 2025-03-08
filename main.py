import logging
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.client import telegram
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import base_ecp
import entry_home
import entry_status
import home_delete
import home_status
import search_date
import search_entry
import search_person
import search_polis
import search_spec_doctor
import search_time
import search_time2
import time_delete
from config.config import bot_token
from handlers import (info_handler, worker_handler, start_handler, person_handler,
                      doctor_handler, return_to_main_menu_handler, spec_handler, po1_handler,
                      po2_handler, po3_handler, po4_handler, time_handler, cancel_handler)
from handlers.doctor_handler import get_doctor
from handlers.spec_handler import get_spec
from handlers.time_handler import get_person_time
from handlers.get_person_handler import get_person_polis
from handlers.entry_handler import entry_person
from handlers.entry_delete_handler import get_delete
from handlers.call_checking import get_person_polis_call
from handlers.call_entry import get_person
from handlers.call_phone import checking_phone
from handlers.call_address import checking_address
from handlers.call_reason_handler import checking_reason
from handlers.call_entry_question_handler import get_person_question

from handlers.cancel_handler import cancel_command, cancel_doctor_command, cancel_home_command
from handlers.cancel_doctor_handler import checking_entry

from keyboards.client_kb import (
    kb_client, spec_client, pol_client, menu_client, ident_client, choise_client, check_client
)
from states.states import ClientRequests
from utils.json_utils import save_user_to_json

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

session = AiohttpSession(
    api=telegram.TelegramAPIServer.from_base('http://95.79.40.128:8081')
)


# Инициализация RedisStorage
#redis_storage = RedisStorage.from_url('redis://95.79.40.128:6379/0')  # Укажите ваш Redis URL

# Инициализация бота и диспетчера
bot = Bot(token=bot_token, session=session)
#dp = Dispatcher(storage=redis_storage)  # Используем RedisStorage
dp = Dispatcher()


# Версия и создатель
version = '5.4.8 release'
creator = '@rapot'
bot_birthday = '13.10.2022 15:14'


# Подключение обработчиков
dp.message.register(start_handler.start_command, Command("start"))
dp.message.register(info_handler.info_command, F.text == "АДРЕСА И ТЕЛЕФОНЫ")
dp.message.register(worker_handler.worker_command, F.text == "РЕЖИМ РАБОТЫ")
dp.message.register(person_handler.get_person_polis, F.text == 'ПРОВЕРКА ВЫЗОВА ВРАЧА НА ДОМ')
dp.message.register(po1_handler.polyclinic_1, F.text == 'ПОЛИКЛИНИКА 1')
dp.message.register(po2_handler.polyclinic_2, F.text == 'ПОЛИКЛИНИКА 2')
dp.message.register(po3_handler.polyclinic_3, F.text == 'ПОЛИКЛИНИКА 3')
dp.message.register(po4_handler.polyclinic_4, F.text == 'ПОЛИКЛИНИКА 4')
dp.message.register(get_spec, ClientRequests.spec)
dp.message.register(get_doctor, ClientRequests.doctor)
dp.message.register(get_person_time, ClientRequests.time)
dp.message.register(get_person_polis, ClientRequests.person)
#dp.message.register(get_delete, ClientRequests.entry_delete)
dp.message.register(entry_person, ClientRequests.entry)
dp.message.register(cancel_handler.cancel_command, F.text == 'ОТМЕНА ЗАПИСИ')
dp.message.register(cancel_handler.cancel_doctor_command, F.text == 'ОТМЕНА ЗАПИСИ К ВРАЧУ')
dp.message.register(cancel_handler.cancel_home_command, F.text == 'ОТМЕНА ЗАПИСИ ВЫЗОВА НА ДОМ')
dp.message.register(checking_entry, ClientRequests.cancel_doctor)
dp.message.register(get_delete, ClientRequests.entry_delete)
dp.message.register(get_person_polis_call, ClientRequests.call_checking)
dp.message.register(get_person, ClientRequests.call_entry)
dp.message.register(checking_address, ClientRequests.call_address)
dp.message.register(checking_phone, ClientRequests.phone)
dp.message.register(checking_reason, ClientRequests.reason)
dp.message.register(get_person_question, ClientRequests.call_entry_question)




async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите раздел:', reply_markup=kb_client)
    logger.info("Пользователь возвращён в главное меню")


@dp.message(F.text == 'вернуться в меню')
async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    await message.answer("Вы вернулись в главное меню.", reply_markup=kb_client)


# Обработчик текстового сообщения "ВЫЗОВ ВРАЧА НА ДОМ"
@dp.message(F.text == "ВЫЗОВ ВРАЧА НА ДОМ")
async def call_home(message: types.Message, state: FSMContext):
    await message.answer('Введите свой полис ОМС: ', reply_markup=menu_client)
    await state.set_state(ClientRequests.call_checking)

# Обработчик состояния call_checking
# @dp.message(ClientRequests.call_checking)
# async def get_person_polis(message: types.Message, state: FSMContext):
#     message_polis = message.text
#
#     if message_polis == 'вернуться в меню':
#         await state.set_state(ClientRequests.main_menu)
#         await message.reply('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     elif len(message_polis) != 16:
#         await message.reply('Неверный ввод, введите 16 цифр номера полиса', reply_markup=menu_client)
#
#     elif not message_polis.isdigit():
#         await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов', reply_markup=menu_client)
#
#     else:
#         await message.answer('Идёт поиск, подождите ', reply_markup=menu_client)
#         polis_data = search_polis.search_polis(message_polis)
#         person = search_person.search_person(polis_data['data'][0]['Person_id'])
#         global person_id
#         person_id = person['data'][0]['Person_id']
#         check_entry_data = entry_status.entry_status(person_id)
#
#         PersonSurName_SurName = person['data'][0]['PersonSurName_SurName']
#         PersonFirName_FirName = person['data'][0]['PersonFirName_FirName']
#         PersonSecName_SecName = person['data'][0]['PersonSecName_SecName']
#         PersonBirthDay_BirthDay = person['data'][0]['PersonBirthDay_BirthDay']
#
#         await message.reply(
#             f' Фамилия: {PersonSurName_SurName}\n'
#             f' Имя: {PersonFirName_FirName}\n'
#             f' Отчество: {PersonSecName_SecName}\n'
#             f' Дата рождения: {PersonBirthDay_BirthDay}\n')
#
#         await message.answer('Это Вы ?', reply_markup=ident_client)
#         await state.set_state(ClientRequests.call_entry)

# Обработчик состояния call_entry
# @dp.message(ClientRequests.call_entry)
# async def get_person(message: types.Message, state: FSMContext):
#     message_entry = message.text
#     print(person_id)
#
#     if message_entry == 'вернуться в меню':
#         await state.set_state(ClientRequests.main_menu)
#         await message.reply('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     elif message_entry == 'ДА':
#         await state.set_state(ClientRequests.call_address)
#         await message.answer('По какому адресу хотите вызвать врача ? (улица, дом, квартира):', reply_markup=menu_client)
#
#     elif message_entry == 'НЕТ':
#         await state.set_state(ClientRequests.main_menu)
#         await message.answer('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     else:
#         await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

# Обработчик состояния call_address
# @dp.message(ClientRequests.call_address)
# async def checking(message: types.Message, state: FSMContext):
#     global address_mess
#     address_mess = message.text
#     print(address_mess)
#     await message.answer(
#         'Введите свой номер телефона (если Вам не смогут дозвонится, вызор будет анулирован:', reply_markup=menu_client)
#     await state.set_state(ClientRequests.phone)

# Обработчик состояния phone
# @dp.message(ClientRequests.phone)
# async def checking(message: types.Message, state: FSMContext):
#     global phone_mess
#     phone_mess = message.text
#     await message.answer('Введите причину вызова,  например (температура, давление):', reply_markup=menu_client)
#     await state.set_state(ClientRequests.reason)

# Обработчик состояния reason
# @dp.message(ClientRequests.reason)
# async def checking_reason(message: types.Message, state: FSMContext):
#     global reason_mess
#     reason_mess = message.text
#     print(reason_mess)
#     print(person_id)
#     await message.answer(f' Вы ввели:\n'
#                          f' Адресс: {address_mess}\n'
#                          f' Телефон: {phone_mess}\n'
#                          f' Причина вызова: {reason_mess}\n'
#                          f'\n'
#                          f' Всё верно ? Отменить запись можно будет только через оператора, '
#                          f'если Вы записываетесь после 12:00, то вызов врача будет назначен'
#                          f' на завтра', reply_markup=ident_client)
#     await state.set_state(ClientRequests.call_entry_question)

# Обработчик состояния call_entry_question
# @dp.message(ClientRequests.call_entry_question)
# async def get_person(message: types.Message, state: FSMContext):
#     message_entry = message.text
#
#     if message_entry == 'вернуться в меню':
#         await state.set_state(ClientRequests.main_menu)
#         await message.reply('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     elif message_entry == 'ДА':
#         await message.answer('Выполняется запрос, ожидайте', reply_markup=kb_client)
#         result_call_entry = entry_home.entry_home(person_id, address_mess, phone_mess, reason_mess)
#         logging.info(f' result_call_entry: {result_call_entry}')
#         if result_call_entry['error_code'] == 6:
#             await state.set_state(ClientRequests.main_menu)
#             await message.answer('У вас уже есть необслуженная запись', reply_markup=kb_client)
#             await message.answer('выберите раздел', reply_markup=kb_client)
#             await state.clear()
#
#         else:
#             HomeVisit_id = result_call_entry['data']['HomeVisit_id']
#             await state.set_state(ClientRequests.main_menu)
#             HomeVisit_setDT = result_call_entry['data']['HomeVisit_setDT']
#             await message.answer(f'Вы успешно записаны, дата записи: {HomeVisit_setDT}\n')
#             await message.answer(f" идентификатор: `{HomeVisit_id}`", parse_mode="Markdown")
#             await state.clear()
#
#     elif message_entry == 'НЕТ':
#         await state.set_state(ClientRequests.main_menu)
#         await message.answer('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     else:
#         await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')


@dp.message(Command(commands=["entry"]))
async def write_command(message: types.Message):
    await message.answer(version, reply_markup=kb_client)


@dp.message(F.text == 'ЗАПИСЬ К ВРАЧУ')
async def spec_command(message: types.Message):
    await message.reply('Выберите поликлинику', reply_markup=pol_client)




@dp.message(F.text == 'ПРОВЕРКА ЗАПИСИ')
async def cancel_command(message: types.Message, state: FSMContext):
    await message.reply('Запись куда хотите проверить ?', reply_markup=check_client)


@dp.message(F.text == 'ПРОВЕРКА ЗАПИСИ К ВРАЧУ')
async def cancel_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите свой полис ОМС: ', reply_markup=menu_client)
    await state.set_state(ClientRequests.checking)

@dp.message(F.text == 'ПРОВЕРКА ВЫЗОВА ВРАЧА НА ДОМ')
async def cancel_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите идентификатор: ', reply_markup=menu_client)
    await state.set_state(ClientRequests.checking_home)


@dp.message(ClientRequests.checking_home)
async def checking(message: types.Message, state: FSMContext):
    mess = message.text
    logger.info(f"Получено сообщение: {mess}")

    # Обработка команды "вернуться в меню"
    if mess == 'вернуться в меню':
        logger.info("Пользователь вернулся в главное меню")
        await return_to_main_menu(message, state)
        return

    # Проверка, что введены только цифры
    if not mess.isdigit():
        await message.reply('Неверный ввод. Вводите только цифры, без символов и пробелов.')
        return

    entry_data_home = home_status.entry_status_home(mess)
    print(f'получено entry_data_home {entry_data_home}')

    status_call = {1: 'новый', 2: 'отказ', 3: 'Одобрен врачом', 4: 'Обслужен', 5: 'Отменен', 6: 'Назначен врач'}

    for entry in entry_data_home['data']:
        await message.reply(
            f"Идентификатор вызова: {mess}\n"
            f"Вызов запланирован на: {entry['HomeVisit_setDT'].split()[0]}\n"
            f"Адрес: {entry['Address_Address']}\n"
            f"Телефон: {entry['HomeVisit_Phone']}\n"
            f"Статус вызова: {status_call[int(entry['HomeVisitWhoCall_id'])]}",
            parse_mode=None
        )

    await return_to_main_menu(message, state)


@dp.message(ClientRequests.cancel_home)
async def cancel_command(message: types.Message, state: FSMContext):
    mess = message.text
    print(mess)
    status_home_delete = home_delete.home_delete(mess)
    logging.info(f' status_home_delete: {status_home_delete}')

    if mess == 'вернуться в меню':
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif status_home_delete['error_code'] == 0:
        await bot.send_message(message.from_user.id, 'Вызов на дом ОТМЕНЁН', reply_markup=menu_client)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif status_home_delete['error_code'] == 6:
        await bot.send_message(message.from_user.id, 'Неверный идентификатор', reply_markup=menu_client)


    else:
        print('test')




async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите раздел:', reply_markup=kb_client)
    logger.info("Пользователь возвращён в главное меню")





changelog = 'реализована отмена'


async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


