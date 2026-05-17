# Кнопки главного меню бота

# Импорты

from aiogram.utils.keyboard import InlineKeyboardBuilder




def get_registration_menu_button():
    """ЕСЛИ АККАУНТА НЕТ В БАЗЕ ДАННЫХ"""

    builder = InlineKeyboardBuilder()

    builder.button(text='Зарегистрироваться', callback_data='registration_btn')
    builder.button(text='Правила', callback_data='rules_btn_register')

    builder.adjust(1)

    return builder.as_markup()


def get_main_menu_button(is_active: bool = False):
    """ГЛАВНОЕ МЕНЮ"""

    builder = InlineKeyboardBuilder()

    builder.button(text='Найти анкету', callback_data='mind_questionnaire')
    builder.button(text='Моя анкета', callback_data='my_questionnaire')

    if is_active:
        btn_active = 'Включить анкету'
    else:
        btn_active = 'Анкета активна'

    builder.button(text=btn_active, callback_data='my_answer')
    builder.button(text='Настройки', callback_data='settings')
    builder.button(text='Центр жалоб', callback_data='complaints')
    builder.button(text='Правила пользования', callback_data='rules_btn')

    builder.adjust(1, 1, 1, 2, 1)

    return builder.as_markup()


def back_to_registration_menu_button():
    """КНОПКА ВОЗВРАТА В РЕГИСТРАЦИЮ"""
    builder = InlineKeyboardBuilder()

    builder.button(text='Вернуться в регистрацию', callback_data='to_registration_menu')

    builder.adjust(1)

    return builder.as_markup()

def back_to_main_menu_button():
    """КНОПКА ВОЗВРАТА"""
    builder = InlineKeyboardBuilder()

    builder.button(text='Вернуться в меню', callback_data='to_main_menu')

    builder.adjust(1)

    return builder.as_markup()


def change_my_questionnaire_button():
    """КНОПКИ ИЗМЕНЕНИЯ АНКЕТЫ"""
    builder = InlineKeyboardBuilder()

    builder.button(text='Изменить анкету', callback_data='change_questionnaire')
    builder.attach(InlineKeyboardBuilder.from_markup(back_to_main_menu_button()))

    builder.adjust(1)

    return builder.as_markup()



def gender_button():
    """КНОПКИ ПОЛА"""
    builder = InlineKeyboardBuilder()

    builder.button(text='Женский', callback_data='gender_female')
    builder.button(text='Мужской', callback_data='gender_male')
    builder.adjust(1)

    return builder.as_markup()


