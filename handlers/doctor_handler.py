from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.client_kb import kb_client
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def get_doctor(message: types.Message, state: FSMContext):
    global spec_dict_final
    mess = message.text
    if mess == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id,
                               'Идёт поиск сводных дат для записи, это может занять много времени, пожалуйста ожидайте..')
        global MedStaffFact_id
        MedStaffFact_id = (spec_dict_final[mess])
        await state.update_data(MedStaffFact_id=MedStaffFact_id)
        data_date_dict = search_date.search_date(MedStaffFact_id)
        data_time_final = search_time.search_time(MedStaffFact_id, data_date_dict)
        if not data_time_final:
            await message.answer('На ближайшие 14 дней нет свободных дат к данному специалисту.')
            await return_to_main_menu(message, state)
        else:
            builder = ReplyKeyboardBuilder()
            builder.row(KeyboardButton(text="вернуться в меню"))
            for i in data_time_final:
                builder.add(KeyboardButton(text=i['TimeTableGraf_begTime']))
            builder.adjust(1, 2)
            markup = builder.as_markup(resize_keyboard=True)
            await message.answer(
                'На ближайшие 14 дня есть следующие свободные даты:\n'
                'Выберите желаемую дату приёма:',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(ClientRequests.time)
            logger.info(f"MedStaffFact_id: {MedStaffFact_id}")