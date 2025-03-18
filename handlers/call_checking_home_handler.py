import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import home_status
from handlers.return_to_main_menu_handler import return_to_main_menu

logger = logging.getLogger(__name__)

async def checking_call_home(message: types.Message, state: FSMContext):
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

    # Используем правильное имя функции и добавляем await
    entry_data_home = await home_status.entry_status(mess)  # Используем await
    print(f'получено entry_data_home {entry_data_home}')

    # Проверка, что данные не пустые
    if not entry_data_home.get('data'):
        await message.reply('Идентификатор не найден. Пожалуйста, введите другой идентификатор.')
        return

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