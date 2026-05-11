# СКРИПТ МОЕЙ АНКЕТЫ


# ИМПОРТЫ
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from buttons.menu_button import back_to_main_menu_button, change_my_questionnaire_button





# СКРИПТ

router = Router()


@router.callback_query(F.data == 'my_questionnaire')
async def change_questionnaire_handlers(callback: CallbackQuery):

    await callback.message.edit_text(
        text='Имя - {}\n'
             'Возраст - {}\n'
             'Инфо - {}\n',
        reply_markup=change_my_questionnaire_button()
    )




