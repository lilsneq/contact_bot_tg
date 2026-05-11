# СКРИПТ КНОПКИ РЕГИСТРАЦИИ


# ИМПОРТЫ

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart


from database.requests import CreateRequests


from buttons.menu_button import get_registration_menu_button, get_main_menu_button



router = Router()


@router.message(CommandStart())
async def cmd_start_handlers(message: Message) -> None:
    """МОДУЛЬ КОТОРЫЙ ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ ПРИ первой инициализации бота"""
    user_id = message.from_user.id

    is_user = await CreateRequests.user_in_bd(user_id)

    if not is_user:
        await message.answer(
            text='Привет, ты у нас в первые.\n'
                 'Нажми на «Зарегистрироваться»,\n'
                 'если согласен с правилами.',
            reply_markup=get_registration_menu_button()
        )

    else:
        await message.answer(
            text='Привет с возвращением',
            reply_markup=get_main_menu_button()
        )



@router.callback_query(F.data == 'registration_btn')
async def register_click_handlers(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    await CreateRequests.set_user_in_bd(user_id)

    await callback.answer('Успешно!')

    await callback.message.answer(
        text='Вы успешно зарегестрировались!',
        reply_markup=get_main_menu_button()
    )

    await callback.message.delete()



