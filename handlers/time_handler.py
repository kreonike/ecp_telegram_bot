from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.client_kb import menu_client, kb_client
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def get_person_time(message: types.Message, state: FSMContext):
    message_time = message.text
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
        data_time_final2 = search_time2.search_time2(MedStaffFact_id, message_time)
        TimeTableGraf_id = data_time_final2[message_time]
        await state.update_data(time=message_time)
        await state.update_data(TimeTableGraf_id=TimeTableGraf_id)
        await state.update_data(message_time=message_time)
        await bot.send_message(message.from_user.id, 'Введите свой полис ОМС: ',
                               reply_markup=menu_client)
        await state.set_state(ClientRequests.person)