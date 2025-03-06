from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.client_kb import spec_client, kb_client
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def get_spec(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Идёт поиск, доступных для записи врачей, ожидайте')
    global spec_dict_final
    question_spec = message.text
    if question_spec == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
    else:
        data_lpu_person = {}
        spec_final = question_spec.lower()
        await state.update_data(spec=spec_final)
        data = await state.get_data()
        spec = data.get('spec')
        pol = data.get('pol')
        base_ecp_medspecoms_id = base_ecp.medspecoms_id
        t = checking_spec = spec_check(spec, base_ecp_medspecoms_id)
        if t == False:
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Неверный ввод специальности, повторите запрос', reply_markup=kb_client)
            await state.clear()
        else:
            base_ecp_spec = base_ecp.medspecoms_id[spec]
            logging.info(f' запрошена специальность: {base_ecp_spec}')
            await state.set_state(ClientRequests.main_menu)
            await state.clear()
            data_lpu_person_old = search_spec_doctor.search_spec_doctor(base_ecp_spec, pol)
            data_lpu_person = [
                item for item in data_lpu_person_old
                if item.get('RecType_id') == '1' and item.get('TimetableGraf_Count') != '0' and item.get('LpuSection_id') != '520101000013118'
            ]
            global post_id
            for key in data_lpu_person:
                post_id = key['Post_id']
            if data_lpu_person == []:
                await bot.send_message(message.from_user.id,
                                       'К данному специалисту запись на 14 ближайших дней отсутствует',
                                       reply_markup=kb_client)
                await state.set_state(ClientRequests.main_menu)
                await state.clear()
            else:
                spec_dict_final = {}
                for i in data_lpu_person:
                    name = i['PersonSurName_SurName']
                    spec_dict_final[name] = i['MedStaffFact_id']
                spec_dict_final = {key.capitalize(): value for key, value in spec_dict_final.items()}
                await state.update_data(spec_dict_final=spec_dict_final)
                def create_doc_keyboard():
                    rows = [list(spec_dict_final.keys())[i:i + 3] for i in range(0, len(spec_dict_final), 3)]
                    keyboard = [
                        [KeyboardButton(text=key) for key in row]
                        for row in rows
                    ]
                    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
                doc = create_doc_keyboard()
                doc.keyboard.insert(0, [KeyboardButton(text="вернуться в меню")])
                await message.reply('К кому хотим записаться?', reply_markup=doc)
                await state.set_state(ClientRequests.doctor)