import enum
from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .user import User


class HabitFrequency(enum.Enum):
    DAILY = "daily"
    # WEEKLY = "weekly" # Можно добавить в будущем
    # MONTHLY = "monthly"


class Habit(Base):
    __tablename__ = "habits"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    frequency: Mapped[HabitFrequency] = mapped_column(
        Enum(HabitFrequency, name="habit_frequency_enum", native_enum=False),
        default=HabitFrequency.DAILY,
        nullable=False,
    )
    target_days: Mapped[int] = mapped_column(
        Integer,
        default=21,
        nullable=False,
    )  # Сколько дней нужно для выработки
    time_to_remind: Mapped[time | None] = mapped_column(
        Time(timezone=False),
        nullable=True,
    )  # Время без учета часового пояса, хранится как UTC или локальное
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )  # Активна ли привычка в целом (не удалена, не завершена)
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Можно добавить дату начала привычки
    # start_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="habits")
    executions: Mapped[list["HabitExecution"]] = relationship(
        "HabitExecution",
        back_populates="habit",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Habit(id={self.id}, user_id={self.user_id}, name='{self.name}', "
            f"is_active={self.is_active})>"
        )


class HabitExecutionStatus(enum.Enum):
    PENDING = "pending"  # Ожидает выполнения (создается планировщиком)
    DONE = "done"  # Выполнено
    NOT_DONE = "not_done"  # Не выполнено / пропущено


class HabitExecution(Base):
    __tablename__ = "habit_executions"

    habit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
    )
    execution_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
    )  # Дата, на которую запланировано/выполнено
    status: Mapped[HabitExecutionStatus] = mapped_column(
        Enum(
            HabitExecutionStatus,
            name="habit_execution_status_enum",
            native_enum=False,
        ),
        default=HabitExecutionStatus.PENDING,
        nullable=False,
    )
    # Время отправки напоминания
    # notified_at: Mapped[datetime | None] = mapped_column(
    # DateTime(timezone=True),
    # nullable=True,
    # )

    habit: Mapped["Habit"] = relationship("Habit", back_populates="executions")

    # Раскомментировать, если нужна уникальность выполнения для привычки на дату
    # __table_args__ = (
    #     UniqueConstraint(
    #     "habit_id",
    #     "execution_date",
    #     name="uq_habit_execution_date",
    #     ),
    # )

    def __repr__(self) -> str:
        return (
            f"<HabitExecution(id={self.id}, habit_id={self.habit_id}, "
            f"date='{self.execution_date}', status='{self.status.value}')>"
        )
