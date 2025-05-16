"""Репозиторий для работы с моделью User."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.core.logging import api_log as log
from src.api.models.user import User
from src.api.repositories.base_repository import BaseRepository
from src.api.schemas.user_schema import UserSchemaCreate, UserSchemaUpdate


class UserRepository(BaseRepository[User, UserSchemaCreate, UserSchemaUpdate]):
    """
    Репозиторий для выполнения CRUD-операций с моделью User.
    Наследует общие методы от BaseRepository и может содержать
    специфичные для User методы.
    """

    async def get_by_telegram_id(
        self, db_session: AsyncSession, *, telegram_id: int
    ) -> User | None:
        """
        Получает пользователя по его Telegram ID.

        Args:
            db_session: Асинхронная сессия базы данных.
            telegram_id: Уникальный идентификатор пользователя в Telegram.

        Returns:
            Экземпляр модели User или None, если пользователь не найден.
        """
        log.debug(f"Получение пользователя по Telegram ID: {telegram_id}")
        statement = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db_session: AsyncSession, *, username: str
    ) -> User | None:
        """
        Получает пользователя по его username (если он есть).
        Учитывает, что username может быть None, поэтому ищет только если передан.

        Args:
            db_session: Асинхронная сессия базы данных.
            username: Имя пользователя в Telegram.

        Returns:
            Экземпляр модели User или None, если пользователь не найден.
        """
        if not username:  # Не ищем, если username не предоставлен или пустой
            return None
        log.debug(f"Получение пользователя по Username: {username}")
        statement = select(self.model).where(self.model.username == username)
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()

    async def update_by_telegram_id(
        self, db_session: AsyncSession, *, telegram_id: int, obj_in: UserSchemaUpdate
    ) -> User | None:
        """
        Обновляет данные пользователя, найденного по Telegram ID.

        Args:
            db_session: Асинхронная сессия базы данных.
            telegram_id: Telegram ID пользователя для обновления.
            obj_in: Схема Pydantic с данными для обновления.

        Returns:
            Обновленный экземпляр User или None, если пользователь не найден.
        """
        log.debug(f"Обновление пользователя по Telegram ID: {telegram_id}")
        user_to_update = await self.get_by_telegram_id(
            db_session, telegram_id=telegram_id
        )
        if not user_to_update:
            return None
        return await super().update(db_session, db_obj=user_to_update, obj_in=obj_in)
