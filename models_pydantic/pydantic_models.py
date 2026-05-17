# МОДУЛЬ ДЛЯ ФИЛЬТРАЦИИ ЧЕРЕЗ pydantic

# ИМПОРТЫ
from pydantic import BaseModel, Field





# СКРИПТ


class PydanticModelRegistration(BaseModel):
    """КЛАСС ФИЛЬТРАЦИЙ ПРИ РЕГИСТРАЦИИ"""
    username_id: int
    name: str = Field(min_length=1, max_length=255)
    age: int = Field(ge=1, le=999)
    about: str | None = Field(default=None, max_length=255)
    image: str
    city: str = Field(min_length=1, max_length=255)
    gender: str = Field(min_length=1, max_length=7)


