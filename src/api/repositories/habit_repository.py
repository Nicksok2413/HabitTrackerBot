"""Репозиторий для работы с моделью Habit."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload  # Для жадной загрузки связанных объектов

from src.api.core.logging import api_log as log
from src.api.models.habit import Habit
from src.api.repositories.base_repository import BaseRepository
from src.api.schemas.habit_schema import HabitSchemaCreate, HabitSchemaUpdate


class HabitRepository(BaseRepository[Habit, HabitSchemaCreate, HabitSchemaUpdate]):
    """
    Репозиторий для выполнения CRUD-операций с моделью Habit.
    """

    async def get_habits_by_user_id(
        self, db_session: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Habit]:
        """
        Получает список привычек для указанного пользователя с пагинацией.

        Args:
            db_session: Асинхронная сессия базы данных.
            user_id: ID пользователя, чьи привычки нужно получить.
            skip: Количество записей для пропуска.
            limit: Максимальное количество записей.

        Returns:
            Список экземпляров модели Habit.
        """
        log.debug(
            f"Получение привычек для пользователя ID={user_id} (skip={skip}, limit={limit})"
        )
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())  # Например, сначала новые
            .offset(skip)
            .limit(limit)
        )
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def get_active_habits_by_user_id(
        self, db_session: AsyncSession, *, user_id: int
    ) -> Sequence[Habit]:
        """
        Получает список всех активных привычек для указанного пользователя.

        Args:
            db_session: Асинхронная сессия базы данных.
            user_id: ID пользователя.

        Returns:
            Список активных экземпляров модели Habit.
        """
        log.debug(f"Получение активных привычек для пользователя ID={user_id}")
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.is_active)
            .order_by(self.model.time_to_remind)  # Например, по времени напоминания
        )
        result = await db_session.execute(statement)
        return result.scalars().all()

    async def get_habit_with_details(
        self, db_session: AsyncSession, *, habit_id: int, user_id: int
    ) -> Habit | None:
        """
        Получает привычку по ID вместе с ее деталями (например, выполнениями),
        принадлежащую конкретному пользователю.

        Args:
            db_session: Асинхронная сессия базы данных.
            habit_id: ID привычки.
            user_id: ID пользователя, для проверки владения.

        Returns:
            Экземпляр Habit с загруженными деталями или None.
        """
        log.debug(
            f"Получение привычки ID={habit_id} с деталями для пользователя ID={user_id}"
        )
        statement = (
            select(self.model)
            .where(self.model.id == habit_id, self.model.user_id == user_id)
            .options(selectinload(self.model.executions))  # Жадная загрузка выполнений
        )
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()
