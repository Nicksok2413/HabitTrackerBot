"""Схемы Pydantic для модели Habit."""

from datetime import datetime, time

from pydantic import Field

from src.api.schemas.base_schema import BaseSchema


# from src.api.schemas.habit_execution_schema import HabitExecutionSchemaRead # Для вложенных выполнений


class HabitSchemaBase(BaseSchema):
    """Базовая схема для привычки, содержит редактируемые поля."""

    name: str = Field(
        ..., min_length=1, max_length=255, description="Название привычки"
    )
    description: str | None = Field(None, description="Описание привычки")
    time_to_remind: time = Field(
        ..., description="Время дня для отправки напоминания (ЧЧ:ММ)"
    )
    # target_days будет устанавливаться при создании из настроек или переданного значения


class HabitSchemaCreate(HabitSchemaBase):
    """Схема для создания новой привычки."""

    # name, description, time_to_remind наследуются
    # user_id будет взят из JWT токена аутентифицированного пользователя на стороне сервера
    target_days: int | None = Field(
        None,
        gt=0,
        description="Количество дней для формирования привычки (если не указано, используется значение из настроек)",
    )
    # current_streak и max_streak будут 0 по умолчанию в модели
    # is_active будет True по умолчанию в модели


class HabitSchemaUpdate(BaseSchema):
    """Схема для обновления существующей привычки. Все поля опциональны."""

    name: str | None = Field(
        None, min_length=1, max_length=255, description="Новое название привычки"
    )
    description: str | None = Field(None, description="Новое описание привычки")
    time_to_remind: time | None = Field(None, description="Новое время для напоминания")
    target_days: int | None = Field(
        None, gt=0, description="Новое количество дней для формирования привычки"
    )
    is_active: bool | None = Field(None, description="Новый статус активности привычки")
    # current_streak и max_streak не должны обновляться напрямую через API пользователем,
    # они управляются логикой выполнения


class HabitSchemaRead(HabitSchemaBase):
    """Схема для чтения данных привычки (ответа API)."""

    id: int = Field(..., description="ID привычки")
    user_id: int = Field(
        ..., description="ID пользователя, которому принадлежит привычка"
    )
    target_days: int = Field(
        ..., description="Количество дней для формирования привычки"
    )
    is_active: bool = Field(..., description="Статус активности привычки")
    current_streak: int = Field(..., description="Текущая непрерывная серия выполнений")
    max_streak: int = Field(
        ..., description="Максимальная достигнутая непрерывная серия выполнений"
    )
    created_at: datetime = Field(..., description="Время создания привычки")
    updated_at: datetime = Field(
        ..., description="Время последнего обновления привычки"
    )

    # Если нужно будет возвращать выполнения привычки:
    # executions: List["HabitExecutionSchemaRead"] = []


# HabitSchemaRead.model_rebuild() # Для циклических зависимостей
