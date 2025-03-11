import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from api import search_date
from api.search_time import search_time
from handlers.return_to_main_menu_handler import return_to_main_menu
from keyboards.client_kb import kb_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)

async def get_doctor(message: types.Message, state: FSMContext):
    from utils.json_temp_data import load_global_spec_dict_final
    print(f'doctor enter value', load_global_spec_dict_final())
    spec_dict_final = load_global_spec_dict_final()

    mess = message.text
    print(f' message_handler() mess: {mess}')

    if mess == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
    else:
        MedStaffFact_id = spec_dict_final[mess]
        from utils.json_temp_data import save_global_medstafffact_id
        save_global_medstafffact_id(MedStaffFact_id)
        await state.update_data(MedStaffFact_id=MedStaffFact_id)

        """поиск даты"""
        data_date_dict = search_date.search_date(MedStaffFact_id)
        print(f' это дата лист из функции: {data_date_dict}')

        # Передаем bot из глобального контекста
        from main import bot  # Импортируем bot из основного файла
        data_time_final = await search_time(MedStaffFact_id, data_date_dict, bot=bot, message=message)
        print(f' data_time_final = {data_time_final}')

        if not data_time_final:
            await message.answer('На ближайшие 14 дней нет свободных дат к данному специалисту.')
            await return_to_main_menu(message, state)
        else:
            builder = ReplyKeyboardBuilder()
            builder.row(KeyboardButton(text="вернуться в меню"))
            for i in data_time_final:
                builder.add(KeyboardButton(text=i['TimeTableGraf_begTime']))
            builder.adjust(1, 2)

            await message.answer(
                'На ближайшие 14 дня есть следующие свободные даты:\n'
                'Выберите желаемую дату приёма:',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(ClientRequests.time)
            logger.info(f"MedStaffFact_id: {MedStaffFact_id}")