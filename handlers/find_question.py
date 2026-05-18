# МОДУЛЬ ПОИСКА АНКЕТ

# ИМПОРТЫ

from aiogram import F, Router, Bot
from aiogram.client import bot
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


from buttons.menu_button import like_or_dislike_button, back_to_main_menu_button
from buttons.help_for_button import ProfileReactionCallback

from database.requests import FindRequest




# Сам скрипт

router = Router()


@router.callback_query(F.data == 'mind_questionnaire')
async def find_handler(callback: CallbackQuery):
    await callback.answer()

    res_user = callback.from_user.id

    res_city = await FindRequest.get_city(res_user)

    quest = await FindRequest.get_is_active_quest(user_id=res_user, city=str(res_city))

    if not quest:
        try:
            await callback.message.delete()
        except Exception:
            pass

        await callback.message.answer(
            text='Нет анкет для поиска',
            reply_markup=back_to_main_menu_button())
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer_photo(
        photo=quest['image_url'],
        caption=f"Имя: {quest['name']}\n"
                f"Возраст: {quest['age']}\n"
                f"О себе: {quest['text']}\n"
                f"Город: {quest['city']}",
        reply_markup=like_or_dislike_button(target_id=quest['username_id'],)
    )



@router.callback_query(ProfileReactionCallback.filter())
async def profile_reaction_callback(callback: CallbackQuery, callback_data: ProfileReactionCallback, bot: Bot):
    await callback.answer()

    user_id = callback.from_user.id
    target_id = callback_data.target_id
    is_like = callback_data.is_like

    await FindRequest.add_interaction(user_id=user_id, viewed_id=target_id, is_like=is_like)

    if is_like:
        try:
            await bot.send_message(
                chat_id=target_id,
                text=f'Кому-то понравилась ваша анкета! Зайдите в поиск чтобы найти взаимность'
            )
        except:
            pass

    try:
        await callback.message.delete()
    except Exception:
        pass

    await find_handler(callback)








