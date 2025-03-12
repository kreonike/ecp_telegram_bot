import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from api import search_time2
from keyboards.client_kb import menu_client, kb_client
from states.states import ClientRequests
from utils.json_temp_data import save_data_time_final

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


async def get_person_time(message: types.Message, state: FSMContext):
    message_time = message.text
    print(f' message_time: {message_time}')
    await state.update_data(time=message_time)

    if message_time == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        # spec_dict_final = {}
        await state.clear()

    else:
        await message.answer('Проверка возможности записи, ожидайте')
        data = await state.get_data()
        MedStaffFact_id = data.get('MedStaffFact_id')

        print(f' message_time в else: {message_time}')
        data_time_final2 = search_time2.search_time2(MedStaffFact_id, message_time)
        print(f' data_time_final2: {data_time_final2}')

        # Проверка, что введенное время есть в словаре data_time_final2
        if message_time not in data_time_final2:
            print(f'Ошибка: время "{message_time}" не найдено в доступных слотах.')
            await message.answer('Ошибка: не верный ввод. Пожалуйста, выберите время из меню.')
            return

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
