# handlers/history_handler.py
import logging

from aiogram import types

from database.models import UserMessage

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_history(message: types.Message):
    try:
        user_messages = (UserMessage.
                         select().
                         where(UserMessage.user_id == message.from_user.id).
                         order_by(UserMessage.timestamp.desc()).
                         # последние 10 сообщений
                         limit(10))

        if not user_messages:
            await message.answer('У вас нет сохранённых сообщений.')
            return

        response = 'Ваши последние сообщения:\n\n'
        for msg in user_messages:
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            message_text = msg.message_text if msg.message_text else '[Нет текста]'
            response += f'[{timestamp}] {message_text}\n'

        await message.answer(response)

    except Exception as e:
        logger.error(f'Ошибка при получении истории сообщений: {str(e)}', exc_info=True)
        await message.answer('Произошла ошибка при получении истории сообщений.')
