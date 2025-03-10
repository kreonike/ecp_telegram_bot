import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from api import search_date, search_time
from handlers.return_to_main_menu_handler import return_to_main_menu
# from handlers.spec_handler import get_spec
from keyboards.client_kb import kb_client
# from main import return_to_main_menu
from states.states import ClientRequests

# from config.config import global_spec_dict_final


logger = logging.getLogger(__name__)

from utils.json_temp_data import load_global_spec_dict_final
print(f'doctor enter value', load_global_spec_dict_final())
spec_dict_final = load_global_spec_dict_final()

async def get_doctor(message: types.Message, state: FSMContext):
    #global spec_dict_final
    print('test test test')
    print(f't2: {spec_dict_final}')

    mess = message.text
    print(f' message_handler() mess: {mess}')

    if mess == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        # spec_dict_final = {}
        await state.clear()

    else:
        await message.answer(
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
            await message.answer('На ближайшие 14 дней нет свободных дат к данному специалисту.')
            await return_to_main_menu(message, state)
        else:

            builder = ReplyKeyboardBuilder()

            # Добавляем кнопку "вернуться в меню" наверху (на всю ширину ряда)
            builder.row(KeyboardButton(text="вернуться в меню"))

            # Добавляем остальные кнопки из data_time_final
            for i in data_time_final:
                builder.add(KeyboardButton(text=i['TimeTableGraf_begTime']))

            # Группируем все кнопки ниже "вернуться в меню" по 2 в строке
            builder.adjust(1, 2)  # Первый ряд (1 кнопка), остальные по 2

            markup = builder.as_markup(resize_keyboard=True)
            keyboard = builder.as_markup(resize_keyboard=True)

            # Отправляем сообщение с клавиатурой
            await message.answer(
                'На ближайшие 14 дня есть следующие свободные даты:\n'
                'Выберите желаемую дату приёма:',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(ClientRequests.time)

            # Логирование
            logger.info(f"MedStaffFact_id: {MedStaffFact_id}")