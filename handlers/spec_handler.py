from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import base_ecp
#import config.config

from base_ecp import medspecoms_id
print(medspecoms_id)

import search_spec_doctor
from keyboards.client_kb import spec_client, kb_client
# from main import spec_check
from states.states import ClientRequests

import logging

logger = logging.getLogger(__name__)



def spec_check(spec, base_ecp_medspecoms_id):
    return spec in base_ecp_medspecoms_id


async def get_spec(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск, доступных для записи врачей, ожидайте')
    #global spec_dict_final
    #await get_doctor(message, state, spec_dict_final)
    # print(f' на входе в get_spec {spec_dict_final}')
    question_spec = message.text
    if question_spec == 'вернуться в меню':
        await state.set_state(ClientRequests.main_menu)
        await message.reply('выберите раздел', reply_markup=kb_client)
        await state.clear()
        print('выход тут')


    else:
        data_lpu_person = {}
        spec_final = question_spec.lower()
        print(f' получено значение: {question_spec}')
        print(f' изменено на: {spec_final}')

        await state.update_data(spec=spec_final)

        data = await state.get_data()
        spec = data.get('spec')
        pol = data.get('pol')

        print(f' spec = {spec}')
        print(f' pol = {pol}')
        #await ClientRequests.next()

        base_ecp_medspecoms_id = base_ecp.medspecoms_id
        t = checking_spec = spec_check(spec, base_ecp_medspecoms_id)
        if t == False:
            await state.set_state(ClientRequests.main_menu)
            await message.reply('Неверный ввод специальности, повторите запрос', reply_markup=kb_client)
            await state.clear()

        else:

            base_ecp_spec = base_ecp.medspecoms_id[spec]

            # print(f' базовая ид специальности: {base_ecp_spec}')
            logging.info(f' запрошена специальность: {base_ecp_spec}')

            await state.set_state(ClientRequests.main_menu)
            await state.clear()

            data_lpu_person_old = search_spec_doctor.search_spec_doctor(base_ecp_spec, pol)

            print(f' 22 на выходе data_lpu_person_old: {data_lpu_person_old}')
            # data_lpu_person = []
            print(data_lpu_person_old)

            data_lpu_person = [
                item for item in data_lpu_person_old
                if item.get('RecType_id') == '1' and item.get('TimetableGraf_Count') != '0'
            ]



            print(f' HHHHH data_lpu_person: {data_lpu_person}')

            #global post_id

            for key in data_lpu_person:
                post_id = key['Post_id']

            # print(post_id)

            if data_lpu_person == []:
                await message.answer(
                                       'К данному специалисту запись на 14 ближайших дней отсутствует',
                                       reply_markup=kb_client)
                await state.set_state(ClientRequests.main_menu)
                # await message.reply('выберите раздел', reply_markup=kb_client)
                await state.clear()



            else:
                #doc = ReplyKeyboardMarkup(resize_keyboard=True)
                spec_dict_final = {}
                print(f't0: {spec_dict_final}')
                for i in data_lpu_person:
                    name = i['PersonSurName_SurName']
                    spec_dict_final[name] = i['MedStaffFact_id']
                print(f' ? post_id: {post_id}')
                print(f' это dict: {spec_dict_final}')
                spec_dict_final = {key.capitalize(): value for key, value in spec_dict_final.items()}
                await state.update_data(spec_dict_final=spec_dict_final)

                # Функция для создания клавиатуры с кнопками в 3 ряда
                def create_doc_keyboard():
                    # Разбиваем список на группы по 3 элемента
                    rows = [list(spec_dict_final.keys())[i:i + 3] for i in range(0, len(spec_dict_final), 3)]

                    keyboard = [
                        [KeyboardButton(text=key) for key in row]  # Создаем ряд кнопок
                        for row in rows  # Для каждой группы из 3 элементов
                    ]

                    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

                doc = create_doc_keyboard()
                doc.keyboard.insert(0, [KeyboardButton(text="вернуться в меню")])

                # Отправляем сообщение с клавиатурой
                await message.reply('К кому хотим записаться?', reply_markup=doc)
                await state.set_state(ClientRequests.doctor)

                await state.set_state(ClientRequests.doctor)

            # print(f' !! {post_id}')
            print(f't1: {spec_dict_final}')
            from utils.json_temp_data import save_global_spec_dict_final, load_global_spec_dict_final, save_postid, load_postid
            #current_value = load_variable()
            save_global_spec_dict_final(spec_dict_final)
            save_postid(post_id)






            #print(f' final', config.config.global_spec_dict_final)








# def print_global_var():
#     print("Global var in file2:", config.spec_dict_final)