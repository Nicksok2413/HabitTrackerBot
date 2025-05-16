"""Репозиторий для работы с моделью HabitExecution."""

from datetime import date
from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.core.logging import api_log as log
from src.api.models.habit_execution import HabitExecution, HabitExecutionStatus
from src.api.repositories.base_repository import BaseRepository
from src.api.schemas.habit_execution_schema import (
    HabitExecutionSchemaCreate,
    HabitExecutionSchemaUpdate,
)


class HabitExecutionRepository(
    BaseRepository[
        HabitExecution, HabitExecutionSchemaCreate, HabitExecutionSchemaUpdate
    ]
):
    """
    Репозиторий для выполнения CRUD-операций с моделью HabitExecution.
    """

    async def get_execution_by_habit_and_date(
        self, db_session: AsyncSession, *, habit_id: int, execution_date: date
    ) -> HabitExecution | None:
        """
        Получает запись о выполнении привычки на конкретную дату.

        Args:
            db_session: Асинхронная сессия базы данных.
            habit_id: ID привычки.
            execution_date: Дата выполнения.

        Returns:
            Экземпляр HabitExecution или None.
        """
        log.debug(
            f"Получение выполнения для привычки ID={habit_id} на дату {execution_date}"
        )
        statement = select(self.model).where(
            and_(
                self.model.habit_id == habit_id,
                self.model.execution_date == execution_date,
            )
        )
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()

    async def get_executions_for_habit(
        self,
        db_session: AsyncSession,
        *,
        habit_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
        status: HabitExecutionStatus | None = None,
    ) -> Sequence[HabitExecution]:
        """
        Получает список выполнений для привычки за указанный период и/или со статусом.

        Args:
            db_session: Асинхронная сессия базы данных.
            habit_id: ID привычки.
            start_date: Начальная дата периода (включительно).
            end_date: Конечная дата периода (включительно).
            status: Фильтр по статусу выполнения.

        Returns:
            Список экземпляров HabitExecution.
        """
        log.debug(
            f"Получение выполнений для привычки ID={habit_id} "
            f"(period: {start_date}-{end_date}, status: {status})"
        )
        statement = select(self.model).where(self.model.habit_id == habit_id)
        if start_date:
            statement = statement.where(self.model.execution_date >= start_date)
        if end_date:
            statement = statement.where(self.model.execution_date <= end_date)
        if status:
            statement = statement.where(self.model.status == status)

        statement = statement.order_by(self.model.execution_date.desc())

        result = await db_session.execute(statement)
        return result.scalars().all()

    async def get_last_n_executions(
        self, db_session: AsyncSession, *, habit_id: int, n_days: int
    ) -> Sequence[HabitExecution]:
        """
        Получает последние N записей о выполнении для привычки.

        Args:
            db_session: Асинхронная сессия базы данных.
            habit_id: ID привычки.
            n_days: Количество последних дней/записей.

        Returns:
            Список экземпляров HabitExecution.
        """
        log.debug(f"Получение последних {n_days} выполнений для привычки ID={habit_id}")
        statement = (
            select(self.model)
            .where(self.model.habit_id == habit_id)
            .order_by(self.model.execution_date.desc())
            .limit(n_days)
        )
        result = await db_session.execute(statement)
        return result.scalars().all()
