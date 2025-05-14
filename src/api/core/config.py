"""Конфигурация приложения."""

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# env_path = Path(__file__).parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Основные настройки приложения."""

    # --- Статические настройки ---

    # Название приложения
    PROJECT_NAME: str = "Habit Tracker Bot"
    # Версия API
    API_VERSION: str = "0.1.0"
    # Хост API
    API_HOST: str = "0.0.0.0"
    # Порт API
    API_PORT: int = 8000
    # URL для внутреннего взаимодействия бот -> API
    API_BASE_URL: str = "http://api:8000"
    # Алгоритм подписи JWT
    JWT_ALGORITHM: str = "HS256"
    # Срок годности JWT токена в минутах
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Настройки, читаемые из .env ---

    # Настройки БД
    POSTGRES_USER: str = Field(..., description="Имя пользователя PostgreSQL")
    POSTGRES_PASSWORD: str = Field(..., description="Пароль PostgreSQL")
    POSTGRES_DB: str = Field(..., description="Название базы данных")
    POSTGRES_HOST: str = Field(
        default="db",
        description="Хост PostgreSQL (название сервиса в Docker)",
    )
    POSTGRES_PORT: int = Field(default=5432, description="Порт PostgreSQL")

    # Настройки безопасности
    API_BOT_SHARED_KEY: str = Field(
        ...,
        description="Ключ для аутентификации бота на стороне API",
    )
    BOT_TOKEN: str = Field(..., description="Токен бота")
    JWT_SECRET_KEY: str = Field(..., description="JWT")

    # Прочие настройки
    DAYS_TO_FORM_HABIT: int = Field(
        default=21,
        description="Количество дней, необходимое для формирования привычки",
    )
    LOG_LEVEL: str = Field(default="INFO", description="Уровень логирования")

    # Настройки Sentry
    SENTRY_DSN: str | None = Field(
        default=None,
        description="Sentry DSN для включения интеграции. Если None, Sentry отключен.",
    )

    # --- Вычисляемые поля ---

    # Формируем URL БД
    @computed_field(repr=False)
    def DATABASE_URL(self) -> str:
        """URL для БД."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Имена переменных окружения не чувствительны к регистру
        extra="ignore",  # Игнорировать лишние переменные окружения
    )


# Кэшированный экземпляр настроек
settings = Settings()  # type: ignore[call-arg]
