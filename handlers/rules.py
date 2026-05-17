# СКРИПТ КНОПКИ ПРАВИЛ


# ИПОРТЫ

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from buttons.menu_button import back_to_main_menu_button, back_to_registration_menu_button

# СКРИПТ

router = Router()




@router.callback_query(F.data == 'rules_btn')
async def rules_handler(callback: CallbackQuery) -> None:

    await callback.message.edit_text(
        text='ПРАВИЛ НЕТ',
        reply_markup=back_to_main_menu_button()
    )

@router.callback_query(F.data == 'rules_btn_register')
async def rules_register_handler(callback: CallbackQuery) -> None:

    await callback.message.edit_text(
        text='ПРАВИЛА СКОРО ПОЯВЯТСЯ',
        reply_markup=back_to_registration_menu_button()
    )













