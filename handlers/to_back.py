# СКРИПТ КНОПКИ ВОЗВРАТА

# ИМПОРТЫ

from aiogram import Router, F
from aiogram.types import CallbackQuery
from buttons.menu_button import get_main_menu_button


# СКРИПТ

router = Router()


@router.callback_query(F.data == 'to_main_menu')
async def process_back(callback: CallbackQuery):
    try:
        await callback.answer()

        if callback.message.photo:
            await callback.message.answer(
                text="Вы вернулись в главное меню:",
                reply_markup=get_main_menu_button()
            )
            await callback.message.delete()

        else:
            await callback.message.edit_text(
                text='Вы вернулись в главное меню:',
                reply_markup=get_main_menu_button()
            )

    except Exception:
        pass