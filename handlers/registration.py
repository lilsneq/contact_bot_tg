# СКРИПТ КНОПКИ РЕГИСТРАЦИИ


# ИМПОРТЫ

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start_handlers(message: Message) -> None:
    user_id = message.from_user.id
    await



