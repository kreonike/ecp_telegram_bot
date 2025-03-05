import logging
import datetime
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage  # Импортируем RedisStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client import telegram
import aiohttp
import json
import redis
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.token import TokenValidationError
from aiogram.fsm.storage.base import StorageKey
from keyboards.client_kb import (
    kb_client, spec_client, pol_client, menu_client, ident_client, choise_client
)
from config import bot_token
import base_ecp
import entry_home
import entry_status
import search_date
import search_entry
import search_person
import search_polis
import search_spec_doctor
import search_time
import search_time2
import time_delete
import home_delete

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
version = '2.2.4 release'
creator = '@rapot'

# Состояния
class ClientRequests(StatesGroup):
    spec = State()
    doctor = State()
    menu = State()
    pol = State()
    doctor_name = State()
    time = State()
    person = State()
    date = State()
    polic = State()
    entry = State()
    TimeTableGraf_id = State()
    person_id = State()
    main_menu = State()
    cancel = State()
    entry_delete = State()
    MedStaffFact_id = State()
    checking = State()
    time_time = State()
    post_id = State()
    message_time = State()
    spec_dict_final = State()
    call_home = State()
    address = State()
    phone = State()
    reason = State()
    call_checking = State()
    call_entry = State()
    call_address = State()
    call_entry_question = State()
    call_entry_finish = State()
    cancel_doctor = State()
    cancel_home = State()
    question_cancel_doctor = State()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(f"Текущее состояние пользователя: {current_state}")
    if current_state:
        await message.answer(f"Восстановлено состояние: {current_state}")
    else:
        await message.reply(
            f' Добро пожаловать,\n'
            f' я бот помошник по ГБУЗ НО ГКБ №12\n'
            f' г.Нижний Новгород, Мочалова, д.8\n'
            f' для получения информации оспользуйтесь кнопками внизу\n'
            f' замечания и предложения: {creator}\n'
            f'\n'
            f' версия бота: {version}\n', reply_markup=kb_client)


# Обработчик текстового сообщения "АДРЕСА И ТЕЛЕФОНЫ"
@dp.message(F.text == "АДРЕСА И ТЕЛЕФОНЫ")
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

# Обработчик текстового сообщения "режим работы"
@dp.message(F.text == "режим работы")
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
@dp.message(ClientRequests.call_checking)
async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text

    if message_polis == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif len(message_polis) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса', reply_markup=menu_client)

    elif not message_polis.isdigit():
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов', reply_markup=menu_client)

    else:
        await message.answer('Идёт поиск, подождите ', reply_markup=menu_client)
        polis_data = search_polis.search_polis(message_polis)
        person = search_person.search_person(polis_data['data'][0]['Person_id'])
        global person_id
        person_id = person['data'][0]['Person_id']
        check_entry_data = entry_status.entry_status(person_id)

        PersonSurName_SurName = person['data'][0]['PersonSurName_SurName']
        PersonFirName_FirName = person['data'][0]['PersonFirName_FirName']
        PersonSecName_SecName = person['data'][0]['PersonSecName_SecName']
        PersonBirthDay_BirthDay = person['data'][0]['PersonBirthDay_BirthDay']

        await message.reply(
            f' Фамилия: {PersonSurName_SurName}\n'
            f' Имя: {PersonFirName_FirName}\n'
            f' Отчество: {PersonSecName_SecName}\n'
            f' Дата рождения: {PersonBirthDay_BirthDay}\n')

        await message.answer('Это Вы ?', reply_markup=ident_client)
        await state.set_state(ClientRequests.call_entry)

# Обработчик состояния call_entry
@dp.message(ClientRequests.call_entry)
async def get_person(message: types.Message, state: FSMContext):
    message_entry = message.text
    print(person_id)

    if message_entry == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif message_entry == 'ДА':
        await state.set_state(ClientRequests.call_address)
        await message.answer('По какому адресу хотите вызвать врача ? (улица, дом, квартира):', reply_markup=menu_client)

    elif message_entry == 'НЕТ':
        await state.set_state(ClientRequests.main_menu)
        await message.answer('выберите раздел', reply_markup=kb_client)
        await state.clear()

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

# Обработчик состояния call_address
@dp.message(ClientRequests.call_address)
async def checking(message: types.Message, state: FSMContext):
    global address_mess
    address_mess = message.text
    print(address_mess)
    await message.answer(
        'Введите свой номер телефона (если Вам не смогут дозвонится, вызор будет анулирован:', reply_markup=menu_client)
    await state.set_state(ClientRequests.phone)

# Обработчик состояния phone
@dp.message(ClientRequests.phone)
async def checking(message: types.Message, state: FSMContext):
    global phone_mess
    phone_mess = message.text
    await message.answer('Введите причину вызова,  например (температура, давление):', reply_markup=menu_client)
    await state.set_state(ClientRequests.reason)

# Обработчик состояния reason
@dp.message(ClientRequests.reason)
async def checking(message: types.Message, state: FSMContext):
    global reason_mess
    reason_mess = message.text
    print(reason_mess)
    print(person_id)
    await message.answer(f' Вы ввели:\n'
                         f' Адресс: {address_mess}\n'
                         f' Телефон: {phone_mess}\n'
                         f' Причина вызова: {reason_mess}\n'
                         f'\n'
                         f' Всё верно ? Отменить запись можно будет только через оператора, '
                         f'если Вы записываетесь после 12:00, то вызов врача будет назначен'
                         f' на завтра', reply_markup=ident_client)
    await state.set_state(ClientRequests.call_entry_question)

# Обработчик состояния call_entry_question
@dp.message(ClientRequests.call_entry_question)
async def get_person(message: types.Message, state: FSMContext):
    message_entry = message.text

    if message_entry == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()

    elif message_entry == 'ДА':
        await message.answer('Выполняется запрос, ожидайте', reply_markup=kb_client)
        result_call_entry = entry_home.entry_home(person_id, address_mess, phone_mess, reason_mess)
        logging.info(f' result_call_entry: {result_call_entry}')
        if result_call_entry['error_code'] == 6:
            await state.set_state(ClientRequests.main_menu)
            await message.answer('У вас уже есть необслуженная запись', reply_markup=kb_client)
            await message.answer('выберите раздел', reply_markup=kb_client)
            await state.clear()

        else:
            HomeVisit_id = result_call_entry['data']['HomeVisit_id']
            await state.set_state(ClientRequests.main_menu)
            HomeVisit_setDT = result_call_entry['data']['HomeVisit_setDT']
            await message.answer(f'Вы успешно записаны, дата записи: {HomeVisit_setDT}\n')
            await message.answer(f" идентификатор: `{HomeVisit_id}`", parse_mode="Markdown")
            await state.clear()

    elif message_entry == 'НЕТ':
        await state.set_state(ClientRequests.main_menu)
        await message.answer('выберите раздел', reply_markup=kb_client)
        await state.clear()

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')


@dp.message(Command(commands=["entry"]))
async def write_command(message: types.Message):
    await message.answer(version, reply_markup=kb_client)


@dp.message(F.text == 'ЗАПИСЬ К ВРАЧУ')
async def spec_command(message: types.Message):
    await message.reply('Выберите поликлинику', reply_markup=pol_client)

@dp.message(F.text == 'ПОЛИКЛИНИКА 1')
async def polyclinic_1(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000000589')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)

@dp.message(F.text == 'ПОЛИКЛИНИКА 2')
async def polyclinic_2(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000000591')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)

@dp.message(F.text == 'ПОЛИКЛИНИКА 3')
async def polyclinic_3(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000001382')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)

@dp.message(F.text == 'ПОЛИКЛИНИКА 4')
async def polyclinic_4(message: types.Message, state: FSMContext):
    await state.update_data(pol='520101000000181')
    await message.reply('Выберите специальность', reply_markup=spec_client)
    await state.set_state(ClientRequests.spec)


@dp.message(F.text == 'ПРОВЕРКА ЗАПИСИ')
async def cancel_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите свой полис ОМС: ', reply_markup=menu_client)
    await state.set_state(ClientRequests.checking)





@dp.message(ClientRequests.checking)
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

    # Проверка длины номера полиса
    if len(mess) != 16:
        await message.reply('Неверный ввод. Номер полиса должен содержать 16 цифр.')
        return

    # Поиск данных по полису
    logger.info("Поиск данных по полису...")
    polis_data = search_polis.search_polis(mess)

    if not polis_data['data']:
        logger.warning("Полис не найден")
        await message.reply('Неверный ввод. Такого полиса не существует.')
        return

    # Получение данных о человеке
    person_id = polis_data['data'][0]['Person_id']
    person_data = search_person.search_person(person_id)

    if not person_data['data']:
        logger.error("Данные о человеке не найдены")
        await message.reply('Ошибка: данные о человеке не найдены.')
        return

    # Получение данных о записях
    entry_data = entry_status.entry_status(person_id)

    if not entry_data['data']['TimeTable']:
        logger.info("Записей на приём не найдено")
        await message.reply('Записей на приём не найдено.')
        await return_to_main_menu(message, state)
        return

    # Отображение информации о записях
    for key in entry_data['data']['TimeTable']:
        name = key['Post_name']
        time = key['TimeTable_begTime']
        id = key['TimeTable_id']
        await message.answer(
            f'Вы записаны к: {name}\n'
            f'На время: {time}\n'
            f'ID бирки: `{id}`',
            parse_mode="Markdown"
        )

    # Возврат в главное меню
    await return_to_main_menu(message, state)

@dp.message(F.text == 'ОТМЕНА ЗАПИСИ')
async def cancel_command(message: types.Message):
    await message.answer('Выберите раздел:', reply_markup=choise_client)

@dp.message(F.text == 'ОТМЕНА ЗАПИСИ К ВРАЧУ')
async def cancel_doctor_command(message: types.Message, state: FSMContext):
    await message.answer('Введите свой полис ОМС:', reply_markup=menu_client)
    logger.info('ОТМЕНА ЗАПИСИ К ВРАЧУ')
    await state.set_state(ClientRequests.cancel_doctor)

@dp.message(F.text == 'ОТМЕНА ЗАПИСИ ВЫЗОВА НА ДОМ')
async def cancel_home_command(message: types.Message, state: FSMContext):
    await message.answer('Отменить вызов врача на дом невозможно. Ожидайте звонка оператора.', reply_markup=kb_client)
    await state.clear()
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


@dp.message(ClientRequests.cancel_doctor)
async def checking(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск, подождите...', reply_markup=menu_client)
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

    # Проверка длины номера полиса
    if len(mess) != 16:
        await message.reply('Неверный ввод. Номер полиса должен содержать 16 цифр.')
        return

    # Поиск данных по полису
    logger.info("Поиск данных по полису...")
    polis_data = search_polis.search_polis(mess)

    if not polis_data['data']:
        logger.warning("Полис не найден")
        await message.reply('Неверный ввод. Такого полиса не существует.')
        return

    # Получение данных о человеке
    person_id = polis_data['data'][0]['Person_id']
    person_data = search_person.search_person(person_id)

    if not person_data['data']:
        logger.error("Данные о человеке не найдены")
        await message.reply('Ошибка: данные о человеке не найдены.')
        return

    # Получение данных о записях
    entry_data = entry_status.entry_status(person_id)
    await state.update_data(entry_data_delete=entry_data)

    if not entry_data['data']['TimeTable']:
        logger.info("Записей на приём не найдено")
        await message.answer('ЗАПИСЕЙ НА ПРИЁМ НЕ НАЙДЕНО.')
        await return_to_main_menu(message, state)
        return

    # Отображение информации о записях
    for key in entry_data['data']['TimeTable']:
        name = key['Post_name']
        time = key['TimeTable_begTime']
        id = key['TimeTable_id']
        await message.answer(
            f'Вы записаны к: {name}\n'
            f'На время: {time}\n'
            f'ID бирки: `{id}`',
            parse_mode="Markdown"
        )

    # Запрос ID бирки для отмены
    await message.answer('Если желаете отменить запись, введите ID бирки:', reply_markup=menu_client)
    await state.set_state(ClientRequests.entry_delete)

@dp.message(ClientRequests.entry_delete)
async def get_delete(message: types.Message, state: FSMContext):
    message_delete = message.text
    logger.info(f"Получено сообщение для отмены: {message_delete}")

    # Обработка команды "вернуться в меню"
    if message_delete == 'вернуться в меню':
        logger.info("Пользователь вернулся в главное меню")
        await return_to_main_menu(message, state)
        return

    # Проверка, что введены только цифры
    if not message_delete.isdigit():
        await message.reply('Неверный ввод. Вводите только цифры, без символов и пробелов.', reply_markup=menu_client)
        return

    # Отмена записи
    data = await state.get_data()
    entry_data = data.get('entry_data_delete')
    del_status = del_entry(message_delete, entry_data)
    logger.info(f"Результат отмены записи: {del_status}")

    if del_status == '0':
        await message.answer('БИРКА УДАЛЕНА.', reply_markup=kb_client)
        await return_to_main_menu(message, state)
    elif del_status == '6':
        await message.answer('Бирка не найдена. Повторите ввод.', reply_markup=menu_client)
    else:
        await message.answer('Неверный ID бирки. Повторите попытку.', reply_markup=menu_client)

async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите раздел:', reply_markup=kb_client)
    logger.info("Пользователь возвращён в главное меню")


def del_entry(message_delete, entry_data):
    print(message_delete)
    print(entry_data)
    del_error = ''
    for key in entry_data['data']['TimeTable']:
        if key['TimeTable_id'] == message_delete:
            print('TimeTable_id = message_delete')
            TimeTableSource = 'Graf'
            status_del = time_delete.time_delete(message_delete, TimeTableSource)
            print(f' status_del: ! {status_del}')

            if status_del['data'] == []:
                print('done')
                del_error = '0'
                return del_error

        elif key['TimeTable_id'] != message_delete:
            print(f' error {del_error}')
            del_error = '6'
            print(del_error)
            return del_error


def spec_check(spec, base_ecp_medspecoms_id):
    return spec in base_ecp_medspecoms_id


# spec_client.add(menu)
@dp.message(ClientRequests.spec)
async def get_spec(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Идёт поиск, доступных для записи врачей, ожидайте')
    global spec_dict_final
    # print(f' на входе в get_spec {spec_dict_final}')
    question_spec = message.text
    if question_spec == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
        print('выход тут')


    else:
        data_lpu_person = {}
        spec_final = question_spec.lower()
        print(f' получено значение: {question_spec}')
        print(f' изменено на: {spec_final}')

        await state.update_data(spec=spec_final)

        data = await state.get_data()
        spec = data.get('spec')
        pol = data.get('pol')

        print(f' spec = {spec}')
        print(f' pol = {pol}')
        #await ClientRequests.next()

        base_ecp_medspecoms_id = base_ecp.medspecoms_id
        t = checking_spec = spec_check(spec, base_ecp_medspecoms_id)
        if t == False:
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Неверный ввод специальности, повторите запрос', reply_markup=kb_client)
            await state.clear()

        else:

            base_ecp_spec = base_ecp.medspecoms_id[spec]

            # print(f' базовая ид специальности: {base_ecp_spec}')
            logging.info(f' запрошена специальность: {base_ecp_spec}')

            await state.set_state(ClientRequests.main_menu)
            await state.clear()

            data_lpu_person_old = search_spec_doctor.search_spec_doctor(base_ecp_spec, pol)

            print(f' 22 на выходе data_lpu_person_old: {data_lpu_person_old}')
            data_lpu_person = []
            print(data_lpu_person_old)
            for key in data_lpu_person_old:
                # print(key)
                if key['Post_id'] != '520101000000049' and key[
                    'Person_id'] != '5656886' and \
                        key['Person_id'] != '7611212' and key['Person_id'] != '10168043' \
                        and key['Person_id'] != '5570722' and key['Person_id'] != '7409255' \
                        and key['Person_id'] != '7511183' and key['Person_id'] != '9827128' \
                        and key['Person_id'] != '9901773' and key['Person_id'] != '9931987' \
                        and key['Person_id'] != '10362016' and key['Person_id'] != '7437558' \
                        and key['Person_id'] != '5656924' and key['Person_id'] != '7193169':
                    data_lpu_person.append(key)
                    # print(key)

            print(f' HHHHH data_lpu_person: {data_lpu_person}')

            global post_id

            for key in data_lpu_person:
                post_id = key['Post_id']

            # print(post_id)

            if data_lpu_person == []:
                await bot.send_message(message.from_user.id,
                                       'К данному специалисту запись на 5 ближайших дней отсутствует',
                                       reply_markup=kb_client)
                await state.set_state(ClientRequests.main_menu)
                # await message.reply('выберите раздел', reply_markup=kb_client)
                await state.clear()



            else:
                #doc = ReplyKeyboardMarkup(resize_keyboard=True)
                spec_dict_final = {}
                print(f't0: {spec_dict_final}')
                for i in data_lpu_person:
                    name = i['PersonSurName_SurName']
                    spec_dict_final[name] = i['MedStaffFact_id']
                print(f' ? post_id: {post_id}')
                print(f' это dict: {spec_dict_final}')
                spec_dict_final = {key.capitalize(): value for key, value in spec_dict_final.items()}
                await state.update_data(spec_dict_final=spec_dict_final)

                # Функция для создания клавиатуры с кнопками в 3 ряда
                def create_doc_keyboard():
                    # Разбиваем список на группы по 3 элемента
                    rows = [list(spec_dict_final.keys())[i:i + 3] for i in range(0, len(spec_dict_final), 3)]

                    # Создаем клавиатуру
                    keyboard = [
                        [KeyboardButton(text=key) for key in row]  # Создаем ряд кнопок
                        for row in rows  # Для каждой группы из 3 элементов
                    ]

                    # Возвращаем клавиатуру
                    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

                # Пример использования
                doc = create_doc_keyboard()


                # # Способ 1: Использование ReplyKeyboardMarkup
                # doc = ReplyKeyboardMarkup(
                #     keyboard=[
                #         [KeyboardButton(text=key)] for key in spec_dict_final  # Кнопки для врачей
                #     ],
                #     resize_keyboard=True
                # )

                # Добавляем кнопку "вернуться в меню" в начало списка
                doc.keyboard.insert(0, [KeyboardButton(text="вернуться в меню")])

                # Отправляем сообщение с клавиатурой
                await message.reply('К кому хотим записаться?', reply_markup=doc)
                await state.set_state(ClientRequests.doctor)

                await state.set_state(ClientRequests.doctor)

            # print(f' !! {post_id}')
            print(f't1: {spec_dict_final}')


@dp.message(ClientRequests.doctor)
async def get_doctor(message: types.Message, state: FSMContext):
    global spec_dict_final
    print('test test test')
    # data = await state.get_data()
    # spec_dict_final = data.get('spec_dict_final')
    print(spec_dict_final)
    # await message.reply('К кому хотим записаться ?', reply_markup=doc)
    # global spec_dict_final
    # print(post_id)

    print(f't2: {spec_dict_final}')

    mess = message.text
    print(f' message_handler() mess: {mess}')

    if mess == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        # spec_dict_final = {}
        await state.clear()

    else:
        await bot.send_message(message.from_user.id,
                               'Идёт поиск сводных дат для записи, это может занять много времени, пожалуйста ожидайте..')
        global MedStaffFact_id

        MedStaffFact_id = (spec_dict_final[mess])
        await state.update_data(MedStaffFact_id=MedStaffFact_id)  ################

        print(f' @@ MedStaffFact_id: {MedStaffFact_id}')

        """поиск даты"""
        data_date_dict = {}
        data_date_dict = search_date.search_date(MedStaffFact_id)
        print(f' это дата лист из функции: {data_date_dict}')

        data_time_final = search_time.search_time(MedStaffFact_id, data_date_dict)
        print(f' data_time_final = {data_time_final}')

        if not data_time_final:
            # Если свободных дат нет
            await message.answer('На ближайшие 4 дня нет свободных дат к данному специалисту.')
            await return_to_main_menu(message, state)
        else:
            # Создаем клавиатуру
            builder = ReplyKeyboardBuilder()

            # Добавляем кнопку "вернуться в меню" наверху
            builder.row(KeyboardButton(text="вернуться в меню"))

            # Добавляем остальные кнопки
            for i in data_time_final:
                builder.add(KeyboardButton(text=i['TimeTableGraf_begTime']))

            # Группируем кнопки по 2 в строке (кроме кнопки "вернуться в меню")
            builder.adjust(3)

            # Получаем клавиатуру
            keyboard = builder.as_markup(resize_keyboard=True)

            # Отправляем сообщение с клавиатурой
            await message.answer(
                'На ближайшие 4 дня есть следующие свободные даты:\n'
                'Выберите желаемую дату приёма:',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(ClientRequests.time)

            # Логирование
            logger.info(f"MedStaffFact_id: {MedStaffFact_id}")



@dp.message(ClientRequests.time)
async def get_person_time(message: types.Message, state: FSMContext):
    message_time = message.text
    print(f' message_time: {message_time}')
    await state.update_data(time=message_time)

    if message_time == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()

    else:
        await bot.send_message(message.from_user.id, 'Проверка возможности записи, ожидайте')
        global data_time_final
        data = await state.get_data()
        MedStaffFact_id = data.get('MedStaffFact_id')

        print(f' message_time в else: {message_time}')
        data_time_final2 = search_time2.search_time2(MedStaffFact_id, message_time)
        print(f' data_time_final2: {data_time_final2}')
        TimeTableGraf_id = data_time_final2[message_time]

        print(f' TimeTableGraf_id !!!!!!!!: {TimeTableGraf_id}')
        print(f' message_time: {message_time}')
        await state.update_data(time=message_time)
        await state.update_data(TimeTableGraf_id=TimeTableGraf_id)
        await state.update_data(message_time=message_time)
        # TimeTableGraf_id

        await bot.send_message(message.from_user.id, 'Введите свой полис ОМС: ',
                               reply_markup=menu_client)
        await state.set_state(ClientRequests.person)


@dp.message(ClientRequests.person)
async def get_person_polis(message: types.Message, state: FSMContext):
    message_polis = message.text
    print(f' message_polis: {message_polis}')

    if message_polis == 'вернуться в меню':
        print('@@вернуться в главное меню')
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()

    elif len(message_polis) != 16:
        await message.reply('Неверный ввод, введите 16 цифр номера полиса',
                            reply_markup=menu_client)

    elif message_polis.isdigit() == False:
        await message.reply('Неверный ввод, вводите только цифры, без символов и пробелов',
                            reply_markup=menu_client)


    elif message_polis.isdigit() == True:
        await bot.send_message(message.from_user.id, 'Идёт поиск, подождите ',
                               reply_markup=menu_client)
        polis_data = search_polis.search_polis(message_polis)
        print(f' polis_num из функции: {polis_data}')
        person = search_person.search_person(polis_data['data'][0]['Person_id'])
        person_id = person['data'][0]['Person_id']
        print(f' получена из функции: {person_id}')

        print('=========ПРОВЕРКА=========')
        print(f' post_id для check: {post_id}')
        print(f' Person_id: {person_id}')
        check_entry_data = entry_status.entry_status(person_id)
        print(check_entry_data)

        data = await state.get_data()
        message_time = data.get('message_time')
        print(message_time)
        date_whithout_time = message_time.partition(' ')[0]

        print(post_id)
        print(check_entry_data)
        print(date_whithout_time)
        global check_error
        check_error = 0
        for j in check_entry_data['data']['TimeTable']:
            if j['Post_id'] == post_id and j['TimeTable_begTime'].partition(' ')[
                0] == date_whithout_time:
                print('НАЙДЕНО СОВПАДЕНИЕ')
                print('запись к одному и тому же специалисту на один и тот же день запрещена')
                check_error = 6

            else:
                print('совпадений не найдено')

        print(check_error)
        await state.update_data(person_id=person_id)

        PersonSurName_SurName = person['data'][0]['PersonSurName_SurName']
        PersonFirName_FirName = person['data'][0]['PersonFirName_FirName']
        PersonSecName_SecName = person['data'][0]['PersonSecName_SecName']
        PersonBirthDay_BirthDay = person['data'][0]['PersonBirthDay_BirthDay']

        await message.reply(
            f' Фамилия: {PersonSurName_SurName}\n'
            f' Имя: {PersonFirName_FirName}\n'
            f' Отчество: {PersonSecName_SecName}\n'
            f' Дата рождения: {PersonBirthDay_BirthDay}\n')

        await bot.send_message(message.from_user.id, 'Это Вы ?', reply_markup=ident_client)

        await state.set_state(ClientRequests.entry)


@dp.message(ClientRequests.entry)
async def get_person(message: types.Message, state: FSMContext):
    message_entry = message.text
    print(message_entry)

    if message_entry == 'вернуться в меню':
        print('вернуться %%%%%%% в главное меню')
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()
        # await ClientRequests.next()

    elif message_entry == 'ДА':
        print(check_error)
        if check_error == 6:

            await state.set_state(ClientRequests.main_menu)
            await message.reply(
                'запись к одному и тому же специалисту на один и тот же день запрещена')
            await state.set_state(ClientRequests.main_menu)
            await message.reply('выберите раздел', reply_markup=kb_client)
            spec_dict_final = {}
            await state.clear()

        elif check_error == 0:
            data = await state.get_data()
            time = data.get('time')
            TimeTableGraf_id = data.get('TimeTableGraf_id')
            person_id = data.get('person_id')

            print(f' message_time: {time}')
            print(f' TimeTableGraf_id: {TimeTableGraf_id}')
            print(f' person_id: {person_id}')

            entry_data = search_entry.search_entry(person_id, TimeTableGraf_id)
            print(f' entry_data: {entry_data}')
            logging.info(f' ЗАПИСЬ {entry_data}')
            await bot.send_message(message.from_user.id,
                                   f" ВЫ УСПЕШНО ЗАПИСАНЫ к:"
                                   f" {entry_data[1]['data']['TimeTable'][0]['Post_name']}"
                                   f" на: {entry_data[1]['data']['TimeTable'][0]['TimeTable_begTime']}\n"
                                   f" приходите к назначенному времени сразу к врачу,\n в регистратуру идти не нужно",
                                   reply_markup=kb_client)

            await state.set_state(ClientRequests.main_menu)
            spec_dict_final = {}
            await state.clear()


        else:
            await bot.send_message(message.from_user.id,
                                   f' возникла какая-то ошибка, сообщите о пробеме @rapot'
                                   f' или попытайтесь позже', reply_markup=menu_client)

    elif message_entry == 'НЕТ':

        await state.set_state(ClientRequests.main_menu)
        await bot.send_message(message.from_user.id, 'выберите раздел',
                               reply_markup=kb_client)
        spec_dict_final = {}
        await state.clear()
        # await ClientRequests.next()


    elif message_entry != 'ДА' or message_entry != 'НЕТ' or message_entry != 'вернуться в меню':
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')

    else:
        await message.reply('Повторите ввод, ДА или НЕТ нажанием на кнопки или словами')




changelog = 'реализована отмена'


async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())