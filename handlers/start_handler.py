import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.client_kb import kb_client
from utils.json_utils import save_user_to_json

logger = logging.getLogger(__name__)


async def start_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    from main import version, creator, bot_birthday
    logger.info(f"Текущее состояние пользователя: {current_state}")
    if current_state:
        await message.answer(f"Восстановлено состояние: {current_state}")
    else:
        await message.reply(
            f' Добро пожаловать,\n'
            f' я бот помощник по ГБУЗ НО ГКБ №12\n'
            f' г.Нижний Новгород, Мочалова, д.8\n'
            f' для получения информации оспользуйтесь кнопками внизу\n'
            f' замечания и предложения: {creator}\n'
            f'\n'
            f' версия бота: {version}\n'
            f' дата создания: {bot_birthday}\n', reply_markup=kb_client)
