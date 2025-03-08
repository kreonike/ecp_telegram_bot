from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import search_date
import search_time
from keyboards.client_kb import kb_client
#from main import return_to_main_menu
from states.states import ClientRequests
import logging

logger = logging.getLogger(__name__)

async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите раздел:', reply_markup=kb_client)
    logger.info("Пользователь возвращён в главное меню")