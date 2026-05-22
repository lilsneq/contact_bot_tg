# Модуль изменения активности анкеты

# Импорты

from aiogram import F, Router
from aiogram.types import CallbackQuery

from buttons.menu_button import get_main_menu_button
from database.requests import CreateRequests


# СКРИПТ

router = Router()


@router.callback_query(F.data == 'my_answer')
async def my_answer_activiti_handler(callback: CallbackQuery):
    """Изменение активности у пользователя"""
    await callback.answer()

    user_id = callback.from_user.id

    res = await CreateRequests.get_boolean_active_user(user_id)
    if res:
        new_status = False
        await CreateRequests.set_boolean_active_user(user_id, False)

        await callback.message.edit_text(
                'Ваша анкета выключена',
                        reply_markup=get_main_menu_button(is_active=new_status))

    else:
        new_status = True
        await CreateRequests.set_boolean_active_user(user_id, True)

        await callback.message.edit_text(
                'Ваша анкета включена',
                        reply_markup=get_main_menu_button(is_active=new_status))














