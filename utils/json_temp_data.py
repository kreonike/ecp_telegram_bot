import json
import os

if not os.path.exists('utils'):
    os.makedirs('utils')

def save_global_spec_dict_final(value):
    file_path = os.path.join('utils', 'global_spec_dict_final.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'c': value}, f, ensure_ascii=False, indent=4)

def load_global_spec_dict_final():
    file_path = os.path.join('utils', 'global_spec_dict_final.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['global_spec_dict_final']
    except FileNotFoundError:
        return {}

def save_data_time_final(value):
    file_path = os.path.join('utils', 'data_time_final.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'data_time_final': value}, f, ensure_ascii=False, indent=4)

def load_data_time_final():
    file_path = os.path.join('utils', 'data_time_final.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['data_time_final']
    except FileNotFoundError:
        return {}

def save_postid(value):
    file_path = os.path.join('utils', 'postid.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'postid': value}, f, ensure_ascii=False, indent=4)

def load_postid():
    file_path = os.path.join('utils', 'postid.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['postid']
    except FileNotFoundError:
        return 0

def save_check_error(value):
    file_path = os.path.join('utils', 'check_error.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'check_error': value}, f, ensure_ascii=False, indent=4)

def load_check_error():
    file_path = os.path.join('utils', 'check_error.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['check_error']
    except FileNotFoundError:
        return 0

def save_global_person_id(value):
    file_path = os.path.join('utils', 'person_id.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'person_id': value}, f, ensure_ascii=False, indent=4)

def load_global_person_id():
    file_path = os.path.join('utils', 'person_id.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['person_id']
    except FileNotFoundError:
        return 0

def save_address_mess(value):
    file_path = os.path.join('utils', 'address_mess.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'address_mess': value}, f, ensure_ascii=False, indent=4)

def load_address_mess():
    file_path = os.path.join('utils', 'address_mess.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['address_mess']
    except FileNotFoundError:
        return 0

def save_phone_mess(value):
    file_path = os.path.join('utils', 'phone_mess.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'phone_mess': value}, f, ensure_ascii=False, indent=4)

def load_phone_mess():
    file_path = os.path.join('utils', 'phone_mess.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['phone_mess']
    except FileNotFoundError:
        return 0

def save_reason_mess(value):
    file_path = os.path.join('utils', 'reason_mess.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'reason_mess': value}, f, ensure_ascii=False, indent=4)

def load_reason_mess():
    file_path = os.path.join('utils', 'reason_mess.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['reason_mess']
    except FileNotFoundError:
        return 0

def save_global_medstafffact_id(value):
    file_path = os.path.join('utils', 'reason_mess.json')
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump({'reason_mess': value}, f, ensure_ascii=False, indent=4)

def load_global_medstafffact_id():
    file_path = os.path.join('utils', 'medstafffact_id.json')
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data['medstafffact_id']
    except FileNotFoundError:
        return 0