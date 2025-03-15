import logging

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.client import telegram
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.filters import Command

from config.config import BOT_TOKEN
from database.models import UserMessage, db
from handlers import (info_handler, worker_handler, start_handler, person_handler,
                      return_to_main_menu_handler, po1_handler,
                      po2_handler, po3_handler, po4_handler, cancel_handler, call_checking_home_handler)
from handlers.call_address import checking_address
from handlers.call_checking import get_person_polis_call
from handlers.call_entry import get_person
from handlers.call_entry_question_handler import get_person_question
from handlers.call_home_handler import call_home
from handlers.call_phone import checking_phone
from handlers.call_reason_handler import checking_reason
from handlers.cancel_doctor_handler import checking_entry
from handlers.doctor_handler import get_doctor
from handlers.entry_delete_handler import get_delete
from handlers.entry_handler import entry_person
from handlers.get_person_handler import get_person_polis
from handlers.history_handler import get_history
from handlers.menu_call_check_entry_handler import check_call_command
# from handlers.call_checking_home_handler import checking_call_home
from handlers.menu_check_enrty_handler import menu_check_entry_command
from handlers.menu_doctor_check_entry_handler import check_doctor_command
from handlers.menu_entry_handler import spec_command
from handlers.spec_handler import get_spec
from handlers.time_handler import get_person_time
from states.states import ClientRequests
from aiogram.fsm.storage.redis import RedisStorage

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

session = AiohttpSession(
    api=telegram.TelegramAPIServer.from_base('http://95.79.40.128:8081')
)


# Инициализация RedisStorage
# redis_storage = RedisStorage.from_url('redis://95.79.40.128:6379/0')  # Укажите ваш Redis URL

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, session=session)
# dp = Dispatcher(storage=redis_storage)  # Используем RedisStorage
dp = Dispatcher()



# Версия и создатель
version = '8.4.3 release'
creator = '@rapot'
bot_birthday = '13.10.2022 15:14'


def init_db():
    db.connect()
    db.create_tables([UserMessage], safe=True)
    logger.info("База данных инициализирована")


# Middleware
class MessageLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data):
        logger.debug(f"Получено сообщение: {event.message_id} от {event.from_user.id}")

        try:
            UserMessage.create(
                user_id=event.from_user.id,
                username=event.from_user.username,
                first_name=event.from_user.first_name,
                message_text=event.text
            )
            logger.info(f"Сохранено сообщение: текст={event.text}, user_id={event.from_user.id}")

        except Exception as e:
            logger.error(f"Ошибка при сохранении сообщения {event.message_id}: {str(e)}", exc_info=True)

        return await handler(event, data)


# Регистрация middleware
dp.message.middleware(MessageLoggingMiddleware())


# Подключение обработчиков
dp.message.register(start_handler.start_command, Command('start'))
dp.message.register(get_history, Command('history'))
dp.message.register(info_handler.info_command, F.text == 'АДРЕСА И ТЕЛЕФОНЫ')
dp.message.register(worker_handler.worker_command, F.text == 'РЕЖИМ РАБОТЫ')
# dp.message.register(person_handler.get_person_polis, F.text == 'ПРОВЕРКА ВЫЗОВА ВРАЧА НА ДОМ')
dp.message.register(po1_handler.polyclinic_1, F.text == 'ПОЛИКЛИНИКА 1')
dp.message.register(po2_handler.polyclinic_2, F.text == 'ПОЛИКЛИНИКА 2')
dp.message.register(po3_handler.polyclinic_3, F.text == 'ПОЛИКЛИНИКА 3')
dp.message.register(po4_handler.polyclinic_4, F.text == 'ПОЛИКЛИНИКА 4')
dp.message.register(get_spec, ClientRequests.spec)
dp.message.register(get_doctor, ClientRequests.doctor)
dp.message.register(get_person_time, ClientRequests.time)
dp.message.register(get_person_polis, ClientRequests.person)
# dp.message.register(get_delete, ClientRequests.entry_delete)
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
dp.message.register(call_home, F.text == 'ВЫЗОВ ВРАЧА НА ДОМ')
# dp.message.register(checking_call_home, ClientRequests.checking_home)
dp.message.register(call_checking_home_handler.checking_call_home, ClientRequests.call_checking)
dp.message.register(spec_command, F.text == 'ЗАПИСЬ К ВРАЧУ')

dp.message.register(check_doctor_command, F.text == 'ПРОВЕРКА ЗАПИСИ К ВРАЧУ')
dp.message.register(check_call_command, F.text == 'ПРОВЕРКА ВЫЗОВА ВРАЧА НА ДОМ')
dp.message.register(check_call_command, ClientRequests.checking_home, F.text == 'ЗАПИСЬ К ВРАЧУ')
# dp.message.register(ClientRequests.checking)
dp.message.register(person_handler.get_person_polis, ClientRequests.checking)
dp.message.register(menu_check_entry_command, F.text == 'ПРОВЕРКА ЗАПИСИ')
dp.message.register(return_to_main_menu_handler.return_to_main_menu, F.text == 'вернуться в меню')

# Обработчик по умолчанию для всех сообщений

@dp.message()
async def default_handler(message: types.Message):
    logger.debug(f"Сообщение попало в обработчик по умолчанию: {message.text}")
    await message.answer("Неверный ввод, выберите на интересующий Вас раздел меню")


async def main():
    init_db()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

# не реализованный функционал

# @dp.message(ClientRequests.cancel_home)
# async def cancel_command(message: types.Message, state: FSMContext):
#     mess = message.text
#     print(mess)
#     status_home_delete = home_delete.home_delete(mess)
#     logging.info(f' status_home_delete: {status_home_delete}')
#
#     if mess == 'вернуться в меню':
#         await message.reply('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     elif status_home_delete['error_code'] == 0:
#         await bot.send_message(message.from_user.id, 'Вызов на дом ОТМЕНЁН', reply_markup=menu_client)
#         await message.reply('выберите раздел', reply_markup=kb_client)
#         await state.clear()
#
#     elif status_home_delete['error_code'] == 6:
#         await bot.send_message(message.from_user.id, 'Неверный идентификатор', reply_markup=menu_client)
#
#
#     else:
#         print('test')




# async def vu(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer('Выберите раздел:', reply_markup=kb_client)
#     logger.info("Пользователь возвращён в главное меню")
