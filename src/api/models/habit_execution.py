"""Модель SQLAlchemy для HabitExecution (Выполнение привычки)."""

from datetime import date
from enum import Enum as PyEnum  # Чтобы не конфликтовать с sqlalchemy.Enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .habit import Habit


class HabitExecutionStatus(PyEnum):
    """Статусы выполнения привычки."""

    PENDING = "pending"  # Ожидает выполнения (создается на день)
    DONE = "done"  # Выполнено
    NOT_DONE = "not_done"  # Не выполнено (пропущено)
    SKIPPED = "skipped"  # Пропущено пользователем (уважительная причина)


class HabitExecution(Base):
    """
    Представляет факт выполнения или невыполнения привычки в конкретный день.

    Attributes:
        id: Первичный ключ (унаследован от Base).
        habit_id: Внешний ключ, связывающий выполнение с привычкой.
        execution_date: Дата, на которую зафиксировано выполнение.
        status: Статус выполнения (pending, done, not_done, skipped).
        created_at: Время создания записи (унаследовано от TimestampMixin).
        updated_at: Время последнего обновления записи (унаследовано от TimestampMixin).
        habit: Связь с привычкой, к которой относится это выполнение.
    """

    __tablename__ = "habit_executions"

    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    execution_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[HabitExecutionStatus] = mapped_column(
        SqlEnum(
            HabitExecutionStatus, name="habit_execution_status_enum", create_type=True
        ),
        default=HabitExecutionStatus.PENDING,
        nullable=False,
        index=True,
    )

    # Связи
    habit: Mapped["Habit"] = relationship(back_populates="executions")

    # Можно добавить уникальное ограничение на (habit_id, execution_date)
    # через __table_args__ если необходимо гарантировать одну запись на день на привычку
    # __table_args__ = (
    #     UniqueConstraint("habit_id", "execution_date", name="uq_habit_execution_per_day"),
    # )
