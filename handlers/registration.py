# СКРИПТ КНОПКИ РЕГИСТРАЦИИ


# ИМПОРТЫ

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from database.requests import CreateRequests

from buttons.menu_button import get_registration_menu_button, get_main_menu_button, gender_button


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
        await message.answer('Ведите текст')
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

    await state.set_state(Registration.about)

    await message.answer('Теперь укажите о себе')


@router.message(Registration.about)
async def register_about(message: Message, state: FSMContext) -> None:
    """хэндлер для того чтобы уловить о себе"""
    if not message.text:
        await message.answer('Ведите текст')
        return
    if len(message.text) >= 255:
        await message.answer('О себе не должна занимать больше 255 символов')
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
    if not message.text:
        await message.answer('Ведите текст')
        return

    await state.update_data(city=message.text)

    await state.set_state(Registration.gender)

    await message.answer(
        text='Теперь пришлите свой пол',
        reply_markup=gender_button()
    )



@router.callback_query(Registration.gender)
async def register_gender(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    if callback.data == 'gender_male':
        gender_value = 'male'
    elif callback.data == 'gender_female':
        gender_value = 'female'
    else:
        gender_value = 'other'

    await state.update_data(gender=gender_value)


    ser_data = await state.get_data()
    user_id = callback.from_user.id

    await CreateRequests.set_question(
        user_id=user_id,
        name=ser_data['name'],
        age=ser_data['age'],
        about=ser_data['about'],
        image=ser_data['image'],
        city=ser_data['city'],
        gender=ser_data['gender']
    )

    await state.clear()

    await callback.message.edit_text(
        text=' Вы успешно зарегистрировались!',
        reply_markup=get_main_menu_button()
    )