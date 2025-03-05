from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

# Создаем кнопки
info = KeyboardButton(text='АДРЕСА И ТЕЛЕФОНЫ')
call = KeyboardButton(text='ВЫЗОВ ВРАЧА НА ДОМ')
spec = KeyboardButton(text='ЗАПИСЬ К ВРАЧУ')
cancel = KeyboardButton(text='ОТМЕНА ЗАПИСИ')
cancel_doctor = KeyboardButton(text='ОТМЕНА ЗАПИСИ К ВРАЧУ')
cancel_home = KeyboardButton(text='ОТМЕНА ЗАПИСИ ВЫЗОВА НА ДОМ')
checking = KeyboardButton(text='ПРОВЕРКА ЗАПИСИ')
doctor = KeyboardButton(text='информация о врачах')
woker = KeyboardButton(text='режим работы')

ther = KeyboardButton(text='ТЕРАПЕВТ')
vac = KeyboardButton(text='ВАКЦИНАЦИЯ')
dis = KeyboardButton(text='ДИСПАНСЕРИЗАЦИЯ')
sto = KeyboardButton(text='СТОМАТОЛОГ')
uro = KeyboardButton(text='УРОЛОГ')
vop = KeyboardButton(text='ВОП')
sto_ther = KeyboardButton(text='СТОМАТОЛОГ-ТЕРАПЕВТ')
xir = KeyboardButton(text='ХИРУРГ')
endo = KeyboardButton(text='ЭНДОКРИНОЛОГ')
oto = KeyboardButton(text='ОТОЛОРИНГОЛОГ')
onko = KeyboardButton(text='ОНКОЛОГ')
oftalmo = KeyboardButton(text='ОФТАЛЬМОЛОГ')

pol1 = KeyboardButton(text='ПОЛИКЛИНИКА 1')
pol2 = KeyboardButton(text='ПОЛИКЛИНИКА 2')
choise_pol2_1 = KeyboardButton(text='ПОЛ2 ул. СВОБОДЫ')
choise_pol2_2 = KeyboardButton(text='ПОЛ2 ул. ЯСНАЯ (ВОП)')

pol3 = KeyboardButton(text='ПОЛИКЛИНИКА 3')
pol4 = KeyboardButton(text='ПОЛИКЛИНИКА 4')

text = KeyboardButton(text='М')

yes = KeyboardButton(text='ДА')
no = KeyboardButton(text='НЕТ')

menu = KeyboardButton(text='вернуться в меню')

check_doctor = KeyboardButton(text='ПРОВЕРКА ЗАПИСИ К ВРАЧУ')
check_home_call = KeyboardButton(text='ПРОВЕРКА ВЫЗОВА ВРАЧА НА ДОМ')

def create_kb_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.row(spec, checking)
    builder.row(call, cancel)
    builder.add(info)
    return builder.as_markup(resize_keyboard=True)


def create_spec_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(menu)

    # Первый ряд: Терапевт, Стоматолог, Уролог
    builder.row(ther, sto, uro)

    # Второй ряд: ВОП, Хирург, Эндокринолог
    builder.row(vop, xir, endo)

    # Третий ряд: Отоларинголог, Онколог, Офтальмолог
    builder.row(oto, onko, oftalmo)

    return builder.as_markup(resize_keyboard=True)

def create_pol_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(menu)
    builder.row(pol1, pol2)
    builder.row(pol3, pol4)
    return builder.as_markup(resize_keyboard=True)

def create_menu_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(menu)
    return builder.as_markup(resize_keyboard=True)

def create_ident_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(menu)
    builder.row(yes, no)
    return builder.as_markup(resize_keyboard=True)

def create_choise_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.row(cancel_doctor, cancel_home)
    builder.add(menu)
    return builder.as_markup(resize_keyboard=True)

def create_check_client() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(menu)
    builder.row(check_doctor, check_home_call)
    return builder.as_markup(resize_keyboard=True)

# Экспортируем клавиатуры
kb_client = create_kb_client()
spec_client = create_spec_client()
pol_client = create_pol_client()
menu_client = create_menu_client()
ident_client = create_ident_client()
choise_client = create_choise_client()
check_client = create_check_client()