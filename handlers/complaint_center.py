# МОДУЛЬ ЦЕНТРА ЖАЛОБ

# ИМПОРТЫ

from aiogram import F, Router
from aiogram.types import CallbackQuery

from buttons.menu_button import back_to_main_menu_button


# Сам скрипт

router = Router()


@router.callback_query(F.data == 'complaints')
async def settings_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Жалобы пока не доступны", reply_markup=back_to_main_menu_button())