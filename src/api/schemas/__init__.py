"""Инициализация модуля схем Pydantic."""

from .base_schema import BaseSchema
from .user_schema import (
    UserSchemaBase,
    UserSchemaCreate,
    UserSchemaRead,
    UserSchemaUpdate,
)
from .habit_schema import (
    HabitSchemaBase,
    HabitSchemaCreate,
    HabitSchemaRead,
    HabitSchemaUpdate,
)
from .habit_execution_schema import (
    HabitExecutionSchemaBase,
    HabitExecutionSchemaCreate,
    HabitExecutionSchemaRead,
    HabitExecutionSchemaUpdate,
)
from src.api.models.habit_execution import (
    HabitExecutionStatus,
)  # Экспортируем Enum тоже, если он нужен вовне

__all__ = [
    "BaseSchema",
    "UserSchemaBase",
    "UserSchemaCreate",
    "UserSchemaRead",
    "UserSchemaUpdate",
    "HabitSchemaBase",
    "HabitSchemaCreate",
    "HabitSchemaRead",
    "HabitSchemaUpdate",
    "HabitExecutionSchemaBase",
    "HabitExecutionSchemaCreate",
    "HabitExecutionSchemaRead",
    "HabitExecutionSchemaUpdate",
    "HabitExecutionStatus",  # Экспорт Enum
]

# Выполняем model_rebuild для схем, которые могут иметь циклические зависимости
# с отложенными аннотациями типов (если бы они были активно использованы)
# Пример:
# UserSchemaRead.model_rebuild()
# HabitSchemaRead.model_rebuild()
