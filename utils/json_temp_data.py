import json

def save_global_spec_dict_final(value):
    with open('global_spec_dict_final.json', 'w',  encoding="utf-8") as f:
        json.dump({'global_spec_dict_final': value}, f, ensure_ascii=False, indent=4)

def load_global_spec_dict_final():
    try:
        with open('global_spec_dict_final.json', 'r',  encoding="utf-8") as f:
            data = json.load(f)
            return data['global_spec_dict_final']
    except FileNotFoundError:
        return {}


def save_data_time_final(value):
    with open('data_time_final.json', 'w', encoding="utf-8") as f:
        json.dump({'data_time_final': value}, f, ensure_ascii=False, indent=4)


def load_data_time_final():
    try:
        with open('data_time_final.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['data_time_final']
    except FileNotFoundError:
        return {}


def save_postid(value):
    with open('postid.json', 'w', encoding="utf-8") as f:
        json.dump({'postid': value}, f, ensure_ascii=False, indent=4)


def load_postid():
    try:
        with open('postid.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['postid']
    except FileNotFoundError:
        return 0


def save_check_error(value):
    with open('check_error.json', 'w', encoding="utf-8") as f:
        json.dump({'check_error': value}, f, ensure_ascii=False, indent=4)


def load_check_error():
    try:
        with open('check_error.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['check_error']
    except FileNotFoundError:
        return 0


def save_global_person_id(value):
    with open('person_id.json', 'w', encoding="utf-8") as f:
        json.dump({'person_id': value}, f, ensure_ascii=False, indent=4)


def load_global_person_id():
    try:
        with open('person_id.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['person_id']
    except FileNotFoundError:
        return 0


def save_address_mess(value):
    with open('address_mess.json', 'w', encoding="utf-8") as f:
        json.dump({'address_mess': value}, f, ensure_ascii=False, indent=4)


def load_address_mess():
    try:
        with open('address_mess.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['address_mess']
    except FileNotFoundError:
        return 0


def save_phone_mess(value):
    with open('phone_mess.json', 'w', encoding="utf-8") as f:
        json.dump({'phone_mess': value}, f, ensure_ascii=False, indent=4)


def load_phone_mess():
    try:
        with open('phone_mess.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['phone_mess']
    except FileNotFoundError:
        return 0


def save_reason_mess(value):
    with open('reason_mess.json', 'w', encoding="utf-8") as f:
        json.dump({'reason_mess': value}, f, ensure_ascii=False, indent=4)


def load_reason_mess():
    try:
        with open('reason_mess.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['reason_mess']
    except FileNotFoundError:
        return 0