"""Репозиторий для работы с моделью Habit."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.core.logging import api_log as log
from src.api.models.habit import Habit
from src.api.repositories.base_repository import BaseRepository
from src.api.schemas.habit_schema import HabitSchemaCreate, HabitSchemaUpdate


class HabitRepository(BaseRepository[Habit, HabitSchemaCreate, HabitSchemaUpdate]):
    """
    Репозиторий для выполнения CRUD-операций с моделью Habit.

    Наследует общие методы от BaseRepository и содержит специфичные для Habit методы.
    """

    def __init__(self):
        """Инициализирует репозиторий для модели Habit."""
        super().__init__(model=Habit)

    async def get_habits_by_user_id(
            self, db_session: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Habit]:
        """
        Получает список привычек для указанного пользователя с пагинацией.

        Args:
            db_session (AsyncSession): Асинхронная сессия базы данных.
            user_id (int): ID пользователя, чьи привычки нужно получить.
            skip (int): Количество записей для пропуска.
            limit (int): Максимальное количество записей.

        Returns:
            Sequence[Habit]: Список привычек пользователя.
        """
        log.debug(
            f"Получение привычек для пользователя ID: {user_id} (skip={skip}, limit={limit})"
        )

        habits = await self.get_multi_by_filter(
            db_session,
            self.model.user_id == user_id,
            skip=skip,
            limit=limit,
            order_by=[self.model.created_at.desc()],  # Сортировка по дате создания (сначала новые)
        )

        log.debug(f"Найдено {len(habits)} привычек для пользователя ID: {user_id}.")
        return habits

    async def get_active_habits_by_user_id(
            self, db_session: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Habit]:
        """
        Получает список всех активных привычек для указанного пользователя с пагинацией.

        Args:
            db_session (AsyncSession): Асинхронная сессия базы данных.
            user_id (int): ID пользователя, чьи активные привычки нужно получить..
            skip (int): Количество записей для пропуска.
            limit (int): Максимальное количество записей.

        Returns:
           Sequence[Habit]:  Список активных привычек пользователя.
        """
        log.debug(
            f"Получение активных привычек для пользователя ID: {user_id} (skip={skip}, limit={limit})"
        )

        filters = [self.model.user_id == user_id, self.model.is_active is True]

        habits = await self.get_multi_by_filter(
            db_session,
            *filters,
            skip=skip,
            limit=limit,
            order_by=[
                self.model.time_to_remind.asc(),
                self.model.name.asc(),
            ],  # Сортировка по времени и имени
        )

        log.debug(
            f"Найдено {len(habits)} активных привычек для пользователя ID: {user_id}."
        )
        return habits

    async def get_habit_with_details(
            self, db_session: AsyncSession, *, habit_id: int, user_id: int
    ) -> Habit | None:
        """
        Получает привычку по ID вместе с ее деталями (например, выполнениями),
        принадлежащую конкретному пользователю.

        Args:
            db_session (AsyncSession): Асинхронная сессия базы данных.
            habit_id (int): ID привычки.
            user_id (int): ID пользователя, для проверки владения.

        Returns:
            Habit | None: Экземпляр Habit с загруженными деталями или None.
        """
        log.debug(
            f"Получение привычки ID: {habit_id} с деталями для пользователя ID: {user_id}"
        )

        statement = (
            select(self.model)
            .where(self.model.id == habit_id, self.model.user_id == user_id)
            .options(selectinload(self.model.executions))  # Жадная загрузка выполнений
        )

        result = await db_session.execute(statement)
        return result.scalar_one_or_none()

# Можно добавить методы для поиска привычек, у которых time_to_remind совпадает с текущим,
# для использования планировщиком, если планировщик будет обращаться к API,
# либо если логика планировщика будет в API сервисе.
# Если планировщик работает напрямую с БД, такие методы в API репозитории могут не понадобиться.
