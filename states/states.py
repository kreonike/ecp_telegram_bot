from aiogram.fsm.state import State, StatesGroup

class ClientRequests(StatesGroup):
    spec = State()
    doctor = State()
    menu = State()
    pol = State()
    doctor_name = State()
    time = State()
    person = State()
    date = State()
    polic = State()
    entry = State()
    TimeTableGraf_id = State()
    person_id = State()
    main_menu = State()
    cancel = State()
    entry_delete = State()
    MedStaffFact_id = State()
    checking = State()
    time_time = State()
    post_id = State()
    message_time = State()
    spec_dict_final = State()
    call_home = State()
    address = State()
    phone = State()
    reason = State()
    call_checking = State()
    call_entry = State()
    call_address = State()
    call_entry_question = State()
    call_entry_finish = State()
    cancel_doctor = State()
    cancel_home = State()
    question_cancel_doctor = State()
    checking_home = State()
