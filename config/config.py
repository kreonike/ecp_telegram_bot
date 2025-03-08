bot_token = '7516097499:AAG-CB1QDrTXLtbSa8_oWOGu_drbB_106Vc'
login_ecp = 'bl12_respond'
password_ecp = 'xM5nQo'

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