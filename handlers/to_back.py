# СКРИПТ КНОПКИ ВОЗВРАТА

# ИМПОРТЫ
import logging


from aiogram import Router, F
from aiogram.types import CallbackQuery, ContentType
from buttons.menu_button import get_main_menu_button, get_registration_menu_button


# СКРИПТ

router = Router()


@router.callback_query(F.data == 'to_main_menu')
async def process_back(callback: CallbackQuery):
    try:
        await callback.answer()

        if callback.message.content_type == ContentType.PHOTO:
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

    except Exception as e:
        logging.error(f'ОШИБКА ВОЗВРАТА В ГЛАВНОЕ МЕНЮ {e}')



@router.callback_query(F.data == 'to_registration_menu')
async def back_process_registration(callback: CallbackQuery):
    try:
        await callback.answer()

        if callback.message.text:
            await callback.message.edit_text(
                text="Вы вернулись в регистрацию",
                reply_markup=get_registration_menu_button()
            )

    except Exception as e:
        logging.error(f'ОШИБКА ВОЗВРАТА В МЕНЮ РЕГИСТРАЦИИ {e}')
