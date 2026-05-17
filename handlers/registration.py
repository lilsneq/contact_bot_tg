# СКРИПТ КНОПКИ РЕГИСТРАЦИИ


# ИМПОРТЫ
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from database.requests import CreateRequests

from buttons.menu_button import get_registration_menu_button, get_main_menu_button, gender_button

# pydantic
from models_pydantic.pydantic_models import PydanticModelRegistration
from pydantic import ValidationError

# СКРИПТ

router = Router()

class Registration(StatesGroup):
    name = State()
    age = State()
    about = State()
    image = State()
    city = State()
    gender = State()



@router.message(CommandStart())
async def cmd_start_handlers(message: Message) -> None:
    """МОДУЛЬ КОТОРЫЙ ДОБАВЛЯЕТ ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ ПРИ первой инициализации бота"""
    user_id = message.from_user.id

    is_user = await CreateRequests.user_in_bd(user_id)

    if not is_user:
        await message.answer(
            text='Привет.\n'
                 'Нажми на «Зарегистрироваться»,\n'
                 'если согласен с правилами.',
            reply_markup=get_registration_menu_button()
        )

    else:
        await message.answer(
            text='Привет, с возвращением',
            reply_markup=get_main_menu_button()
        )



@router.callback_query(F.data == 'registration_btn')
async def register_click_handlers(callback: CallbackQuery, state: FSMContext) -> None:
    """ХЕНДЛЕР РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ"""
    await callback.answer()

    #регестрация в бд
    user_id = callback.from_user.id
    await CreateRequests.set_user_in_bd(user_id)


    await state.set_state(Registration.name)
    await callback.message.edit_text('Введите ваше имя!')




@router.message(Registration.name)
async def register_name(message: Message, state: FSMContext) -> None:
    """хэндлер для того чтобы уловить имя"""
    if not message.text:
        await message.answer('Введите текст')
        return

    if len(message.text) >= 255:
        await message.answer('Текс слишком большой')
        return

    await state.update_data(name=message.text)

    await state.set_state(Registration.age)

    await message.answer('Теперь укажите ваш возраст')


@router.message(Registration.age)
async def register_age(message: Message, state: FSMContext) -> None:
    """хэндрел для того чтобы уловить возраст"""

    if not message.text.isdigit():
        await message.answer('Пожалуйста введите возраст цифрами')
        return

    await state.update_data(age=int(message.text))
    await state.update_data(age=message.text)

    await state.set_state(Registration.about)

    await message.answer('Теперь укажите о себе')


@router.message(Registration.about)
async def register_about(message: Message, state: FSMContext) -> None:
    """хэндлер для того чтобы уловить о себе"""

    if not message.text:
        await message.answer('Введите текст')
        return

    if len(message.text) >= 255:
        await message.answer('Текс слишком большой')
        return

    await state.update_data(about=message.text)

    await state.set_state(Registration.image)

    await message.answer('Теперь пришлите своё фото')


@router.message(Registration.image, F.photo)
async def register_image(message: Message, state: FSMContext) -> None:
    """хэндлер для того чтобы уловить фото"""

    photo_id = message.photo[-1].file_id
    if not photo_id:
        await message.answer('Пришлите фото')
        return

    await state.update_data(image=photo_id)

    await state.set_state(Registration.city)

    await message.answer('Теперь пришлите свой город')



@router.message(Registration.city)
async def register_city(message: Message, state: FSMContext) -> None:
    """хендлер для того чтобы уловить город"""

    if not message.text:
        await message.answer('Введите текст')
        return

    if len(message.text) >= 255:
        await message.answer('Текс слишком большой')
        return


    await state.update_data(city=message.text)

    await state.set_state(Registration.gender)

    await message.answer(
        text='Теперь пришлите свой пол',
        reply_markup=gender_button()
    )



@router.callback_query(Registration.gender)
async def register_gender(callback: CallbackQuery, state: FSMContext) -> None:
    """хендлер для того чтобы уловить гендер и отправить анкету в бд"""
    await callback.answer()

    if callback.data == 'gender_male':
        gender_value = 'male'
    elif callback.data == 'gender_female':
        gender_value = 'female'
    else:
        gender_value = 'other'

    await state.update_data(gender=gender_value)


    user_data = await state.get_data()

    user_info_dict = {
        'username_id': callback.from_user.id,
        'name': user_data.get('name', 'нет имени'),
        'age': user_data.get('age', 18),
        'about': user_data.get('about', None),
        'image': user_data.get('image', 'Нет фото'),
        'city': user_data.get('city', 'нет города'),
        'gender': user_data.get('gender', 'male')
    }

    try:
        validated_user = PydanticModelRegistration(**user_info_dict)
        await CreateRequests.set_question(
        user_id=validated_user.username_id,
        name=validated_user.name,
        age=validated_user.age,
        about=validated_user.about,
        image=validated_user.image,
        city=validated_user.city,
        gender=validated_user.gender
        )
        await state.clear()

    except ValidationError as e:
        logging.error(f"ОШИБКА pydantic В БАЗУ ДАННЫХ НИЧЕГО НЕ ДОБАВЛЕНО {e}", exc_info=True)

        await callback.message.edit_text('Ошибка при заполнении анкеты, пожалуйста повторите попытку', reply_markup=get_registration_menu_button())
        await state.clear()
        return

    await callback.message.edit_text(
        text=' Вы успешно зарегистрировались!',
        reply_markup=get_main_menu_button()
    )