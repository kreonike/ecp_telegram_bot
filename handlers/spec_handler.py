from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from handlers import base_ecp
from api import search_spec_doctor
from keyboards.client_kb import kb_client
from states.states import ClientRequests

import logging

logger = logging.getLogger(__name__)


# Функция для проверки наличия специальности в базе
def spec_check(spec, base_ecp_medspecoms_id):
    return spec in base_ecp_medspecoms_id


async def get_spec(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск доступных для записи врачей, ожидайте')

    question_spec = message.text
    if question_spec == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('Выберите раздел', reply_markup=kb_client)
        await state.clear()
        print('Выход из выбора специальности')
    else:
        data_lpu_person = {}
        spec_final = question_spec.lower()
        print(f'Получено значение: {question_spec}')
        print(f'Изменено на: {spec_final}')

        await state.update_data(spec=spec_final)

        data = await state.get_data()
        spec = data.get('spec')
        pol = data.get('pol')

        print(f'Специальность: {spec}')
        print(f'Пол: {pol}')

        # словарь для проверки специальностей
        base_ecp_medspecoms_id = {
            'хирург': base_ecp.MEDSPEC_SURGEON,
            'стоматолог': base_ecp.MEDSPEC_DENTIST,
            'травматолог': base_ecp.MEDSPEC_TRAUMATOLOGIST,
            'статист': base_ecp.MEDSPEC_STATISTICIAN,
            'рентгенолог': base_ecp.MEDSPEC_RADIOLOGIST,
            'медсестра рентгенолога': base_ecp.MEDSPEC_RADIOLOGIST_NURSE,
            'отолоринголог': base_ecp.MEDSPEC_OTOLARYNGOLOGIST,
            'мед сестра': base_ecp.MEDSPEC_NURSE,
            'воп': base_ecp.MEDSPEC_GENERAL_PRACTITIONER,
            'медсестра врача общей практики': base_ecp.MEDSPEC_GENERAL_PRACTITIONER_NURSE,
            'зубной врач': base_ecp.MEDSPEC_DENTAL_DOCTOR,
            'эндокринолог': base_ecp.MEDSPEC_ENDOCRINOLOGIST,
            'гастро': base_ecp.MEDSPEC_GASTROENTEROLOGIST,
            'акушер-гинеколог': base_ecp.MEDSPEC_OBSTETRICIAN_GYNECOLOGIST,
            'уролог': base_ecp.MEDSPEC_UROLOGIST,
            'мед сестра процедурного кабинета': base_ecp.MEDSPEC_PROCEDURE_ROOM_NURSE,
            'инфекционный': base_ecp.MEDSPEC_INFECTIOUS_DISEASE_SPECIALIST,
            'врач-лаборатории': base_ecp.MEDSPEC_LABORATORY_DOCTOR,
            'гематологи': base_ecp.MEDSPEC_HEMATOLOGIST,
            'лаборатория': base_ecp.MEDSPEC_LABORATORY,
            'медсетра палатная': base_ecp.MEDSPEC_WARD_NURSE,
            'невролог': base_ecp.MEDSPEC_NEUROLOGIST,
            'стоматолог-терапевт': base_ecp.MEDSPEC_DENTAL_THERAPIST,
            'пульманолог': base_ecp.MEDSPEC_PULMONOLOGIST,
            'офтальмолог': base_ecp.MEDSPEC_OPHTHALMOLOGIST,
            'кардиолог': base_ecp.MEDSPEC_CARDIOLOGIST,
            'онколог': base_ecp.MEDSPEC_ONCOLOGIST,
            'акушерка': base_ecp.MEDSPEC_MIDWIFE,
            'терапевт': base_ecp.MEDSPEC_THERAPIST,
        }

        t = checking_spec = spec_check(spec, base_ecp_medspecoms_id)
        if t == False:
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Неверный ввод специальности, повторите запрос', reply_markup=kb_client)
            await state.clear()
        else:
            base_ecp_spec = base_ecp_medspecoms_id[spec]

            logging.info(f'Запрошена специальность: {base_ecp_spec}')

            await state.set_state(ClientRequests.main_menu)
            await state.clear()

            data_lpu_person_old = search_spec_doctor.search_spec_doctor(base_ecp_spec, pol)

            print(f'На выходе data_lpu_person_old: {data_lpu_person_old}')

            data_lpu_person = [
                item for item in data_lpu_person_old
                if item.get('RecType_id') == '1' and item.get('TimetableGraf_Count') != '0'
            ]

            print(f'Отфильтрованные данные: {data_lpu_person}')

            for key in data_lpu_person:
                post_id = key['Post_id']

            if data_lpu_person == []:
                await message.answer(
                    'К данному специалисту запись на 14 ближайших дней отсутствует',
                    reply_markup=kb_client)
                await state.set_state(ClientRequests.main_menu)
                await state.clear()
            else:
                spec_dict_final = {}
                print(f'Начальное состояние spec_dict_final: {spec_dict_final}')
                for i in data_lpu_person:
                    name = i['PersonSurName_SurName']
                    spec_dict_final[name] = i['MedStaffFact_id']
                print(f'Post_id: {post_id}')
                print(f'Словарь врачей: {spec_dict_final}')
                spec_dict_final = {key.capitalize(): value for key, value in spec_dict_final.items()}
                await state.update_data(spec_dict_final=spec_dict_final)

                # Функция для создания клавиатуры с кнопками в 3 ряда
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

                from utils.json_temp_data import save_global_spec_dict_final, save_postid
                save_global_spec_dict_final(spec_dict_final)
                print(f'записываем save_global_spec_dict_final', spec_dict_final)
                save_postid(post_id)

