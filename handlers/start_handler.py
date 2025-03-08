import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import kb_client
from utils.json_utils import save_user_to_json

logger = logging.getLogger(__name__)

# Версия и создатель
version = '4.0.2 '
creator = '@rapot'
bot_birthday = '13.10.2022 15:14'


async def start_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(f"Текущее состояние пользователя: {current_state}")
    if current_state:
        await message.answer(f"Восстановлено состояние: {current_state}")
    else:
        await message.reply(
            f' Добро пожаловать,\n'
            f' я бот помошник по ГБУЗ НО ГКБ №12\n'
            f' г.Нижний Новгород, Мочалова, д.8\n'
            f' для получения информации оспользуйтесь кнопками внизу\n'
            f' замечания и предложения: {creator}\n'
            f'\n'
            f' версия бота: {version}\n'
            f' дата создания: {bot_birthday}\n', reply_markup=kb_client)

        # Собираем данные о пользователе
        user_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "date": message.date.isoformat()
        }

        # Сохраняем данные в JSON
        save_user_to_json(user_data)