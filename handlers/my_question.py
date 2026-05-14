# СКРИПТ МОЕЙ АНКЕТЫ


# ИМПОРТЫ
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from buttons.menu_button import back_to_main_menu_button, change_my_questionnaire_button

from database.requests import CreateRequests




# СКРИПТ

router = Router()


@router.callback_query(F.data == 'my_questionnaire')
async def my_questionnaire_handler(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    data = await CreateRequests.get_question(user_id)
    if not data:
        await callback.message.answer(
            text="Анкета не найдена, создайте её заново",
            reply_markup=change_my_questionnaire_button()
        )
        return

    await callback.message.answer_photo(
        photo=data['image_url'],
        caption=f"   Ваша анкета:\n\n"
                f"Имя: {data['name']}\n"
                f"Возраст: {data['age']}\n"
                f"О себе: {data['text']}\n"
                f"Город: {data['city']}",
        reply_markup=change_my_questionnaire_button()
        )


    await callback.message.delete()







