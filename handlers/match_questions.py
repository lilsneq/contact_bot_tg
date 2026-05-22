# МОДУЛЬ МЭТЧ АНКЕТ
import asyncio
from pyexpat.errors import messages

# ИМПОРТЫ

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery

from buttons.help_for_button import MatchReactionCallback
from buttons.menu_button import back_to_main_menu_button, ProfileReactionCallback, match_questionnaire_button, match_like_or_dislike_button

from database.requests import FindRequest, CreateRequests


# СКРИПТ


router = Router()


@router.callback_query(F.data == 'match_questionnaire')
async def match_questionnaire(callback_query: CallbackQuery):
    await callback_query.answer()

    viewed_id = callback_query.from_user.id
    quest = await FindRequest.get_match_questionnaire(viewed_id)

    if not quest:
        await callback_query.message.edit_text(
            text="Нет взаимных Метчев",
            reply_markup=back_to_main_menu_button()
        )
        await callback_query.answer()
        return

    try:
        await callback_query.message.delete()
    except Exception:
        pass


    for i, user_data  in enumerate(quest):
        caption_text =(f"@{user_data['tg_us'] if not None else 'lilsneq'}\n"
                      f"Имя: {user_data['name']}\n"
                      f"Возраст: {user_data['age']}\n"
                      f"О себе: {user_data['text']}\n"
                      f"Город: {user_data['city']}")

        await callback_query.message.answer_photo(
                photo=user_data['image_url'],
                caption=caption_text,
        )
        await asyncio.sleep(0.3)

    await callback_query.message.answer(
        text="Это все ваши взаимные метчи!",
        reply_markup=back_to_main_menu_button()
    )

    await callback_query.answer()



# @router.callback_query(MatchReactionCallback.filter())
# async def match_reaction_callback(callback: CallbackQuery, callback_data: MatchReactionCallback, bot: Bot):
#     await callback.answer()
#
#     user_id = callback.from_user.id
#     target_id = callback_data.target_id
#     is_like = callback_data.is_like
#
#     is_match = await FindRequest.add_interaction(user_id=user_id, viewed_id=target_id, is_like=is_like)
#
#     if is_match:
#
#         current_user_quest = await CreateRequests.get_question(user_id=user_id)
#         await callback.message.answer(
#             text="Взаимная симпатия! У вас новый мэтч.",
#             reply_markup=match_questionnaire_button()
#         )
#         if current_user_quest:
#             try:
#                 caption_text = (
#                     f"    Взаимная симпатия!\n\n"
#                     f"@{123}\n"
#                     f"Имя: {current_user_quest['name']}\n"
#                     f"Возраст: {current_user_quest['age']}\n"
#                     f"О себе: {current_user_quest['text']}\n"
#                     f"Город: {current_user_quest['city']}"
#                 )
#                 keyboard = match_questionnaire_button(target_id=user_id)
#
#                 await bot.send_photo(
#                     chat_id=target_id,
#                     photo=current_user_quest['image_url'],
#                     caption=caption_text,
#                     reply_markup=keyboard
#                 )
#             except Exception:
#                 # Если не получилось отправить фото, отправляем текстом
#                 try:
#                     await bot.send_message(
#                         chat_id=target_id,
#                         text=f"🎉 Взаимная симпатия!\n\n{caption_text}",
#                         reply_markup=keyboard
#                     )
#                 except Exception:
#                     pass
#
#     elif is_like:
#         try:
#             await bot.send_message(
#                 chat_id=target_id,
#                 text='Кому-то понравилась ваша анкета!',
#                 reply_markup=match_questionnaire_button()
#             )
#         except Exception:
#             pass
#
#     try:
#         await callback.message.delete()
#     except Exception:
#         pass
#
#     await match_questionnaire(callback)