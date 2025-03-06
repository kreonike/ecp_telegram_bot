import json

def save_user_to_json(user_data):
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    users.append(user_data)

    # Записываем обновленный список обратно в файл
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


