# СКРИПТ КНОПКИ РЕГИСТРАЦИИ


# ИМПОРТЫ

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup


from database.requests import CreateRequests

from buttons.menu_button import get_registration_menu_button, get_main_menu_button


# СКРИПТ

router = Router()

class Registration(StatesGroup):
    name = State()
    age = State()
    about = State()
    image = State()



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
    await state.update_data(about=message.text)

    await state.set_state(Registration.image)

    await message.answer('Теперь пришлите своё фото')


@router.message(Registration.image, F.photo)
async def register_image(message: Message, state: FSMContext) -> None:
    """хэндлер для того чтобы уловить фото"""
    photo_id = message.photo[-1].file_id

    ser_data = await state.get_data()
    user_id = message.from_user.id

    await CreateRequests.set_question(
        user_id=user_id,
        name=ser_data['name'],
        age=ser_data['age'],
        about=ser_data['about'],
        image=photo_id
    )

    await state.clear()

    await message.answer(
        text='🎉 Вы успешно зарегистрировались!',
        reply_markup=get_main_menu_button()
    )



