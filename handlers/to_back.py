# СКРИПТ КНОПКИ ВОЗВРАТА

# ИМПОРТЫ

from aiogram import Router, F
from aiogram.types import CallbackQuery
from buttons.menu_button import get_main_menu_button


# СКРИПТ

router = Router()


@router.callback_query(F.data == 'to_main_menu')
async def process_back(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text="Вы вернулись в главное меню:",
        reply_markup=get_main_menu_button()
    )

