# модуль для улучшения кнопок

# ИМПОРТ
from aiogram.filters.callback_data import CallbackData



# СКРИПТ

class ProfileReactionCallback(CallbackData, prefix='reaction'):
    target_id: int
    is_like: bool