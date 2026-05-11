# Кнопки главного меню бота

# Импорты

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_registration_menu_button():
    """ЕСЛИ АККАУНТА НЕТ В БАЗЕ ДАННЫХ"""

    builder = InlineKeyboardBuilder()

    builder.button(text='Зарегистрироваться', callback_data='registration_btn')

    builder.adjust(1)

    return builder.as_markup()


def get_main_menu_button():
    """ГЛАВНОЕ МЕНЮ"""

    builder = InlineKeyboardBuilder()

    builder.button(text='Найти анкету', callback_data='mind_questionnaire')
    builder.button(text='Моя анкета', callback_data='my_questionnaire')
    builder.button(text='Настройки', callback_data='settings')
    builder.button(text='Центр жалоб', callback_data='complaints')

    builder.adjust(1)

    return builder.as_markup()



def back_to_main_menu_button():
    builder = InlineKeyboardBuilder()

    builder.button(text='Вернуться в меню', callback_data='to_main_menu')

    return builder.as_markup()
