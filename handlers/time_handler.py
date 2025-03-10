import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import search_time2
from keyboards.client_kb import menu_client, kb_client
from states.states import ClientRequests

logger = logging.getLogger(__name__)


from utils.json_temp_data import save_data_time_final


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
        await message.answer('Проверка возможности записи, ожидайте')
        #global data_time_final
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
        await message.answer('Введите свой полис ОМС: ',
                               reply_markup=menu_client)
        await state.set_state(ClientRequests.person)
        save_data_time_final(data_time_final2)