# МОДУЛЬ ИЗМЕНЕНИЯ ПРОФИЛЯ

# ИМПОРТЫ
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from handlers.registration import Registration
from buttons.menu_button import change_my_questionnaire_button



# СКРИПТ
router = Router()



@router.callback_query(F.data == 'change_questionnaire')
async def change_questionnaire(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Registration.name)

    await callback.message.answer("Введите имя")







