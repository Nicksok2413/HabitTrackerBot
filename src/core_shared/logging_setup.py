"""Централизованная настройка логирования для всех сервисов проекта."""

import sys
import os
from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field

# Предполагаем, что settings доступны, если этот модуль используется в API
# Для бота и планировщика LOG_LEVEL и SENTRY_DSN будут передаваться явно или читаться из их конфигов
try:
    from src.api.core.config import settings as api_settings
except ImportError:
    api_settings = None  # type: ignore


class LogConfig(BaseModel):
    """Конфигурация логирования."""

    level: str = Field(default="INFO", description="Уровень логирования")
    format: str = Field(
        default=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        ),
        description="Формат лог сообщения",
    )
    rotation: str = Field(default="10 MB", description="Ротация лог-файлов по размеру")
    retention: str = Field(default="7 days", description="Время хранения лог-файлов")
    serialize: bool = Field(default=False, description="Сериализовать логи в JSON")
    enable_file_logging: bool = Field(
        default=True, description="Включить логирование в файл"
    )
    log_file_path: str = Field(
        default="logs/{service_name}_{time:YYYY-MM-DD}.log",
        description="Путь к файлу логов",
    )
    sentry_dsn: Optional[str] = Field(
        default=None, description="DSN для интеграции с Sentry"
    )


def setup_logger(
    service_name: str,
    log_config: Optional[LogConfig] = None,
    log_level_override: Optional[str] = None,
    sentry_dsn_override: Optional[str] = None,
) -> None:
    """
    Настраивает Loguru логгер для указанного сервиса.

    Args:
        service_name: Имя сервиса (например, "API", "Bot", "Scheduler").
        log_config: Объект конфигурации LogConfig. Если None, используются значения по умолчанию.
        log_level_override: Переопределяет уровень логирования из конфигурации.
        sentry_dsn_override: Переопределяет Sentry DSN из конфигурации.
    """
    if log_config is None:
        config = LogConfig()
    else:
        config = log_config

    # Применяем переопределения, если они есть
    if log_level_override:
        config.level = log_level_override
    elif api_settings and hasattr(
        api_settings, "LOG_LEVEL"
    ):  # Пытаемся взять из общих настроек API
        config.level = api_settings.LOG_LEVEL

    if sentry_dsn_override:
        config.sentry_dsn = sentry_dsn_override
    elif api_settings and hasattr(
        api_settings, "SENTRY_DSN"
    ):  # Пытаемся взять из общих настроек API
        config.sentry_dsn = api_settings.SENTRY_DSN

    logger.remove()  # Удаляем все предыдущие обработчики, чтобы избежать дублирования

    # Обработчик для вывода в консоль (stderr)
    logger.add(
        sys.stderr,
        level=config.level.upper(),
        format=config.format.replace(
            "{name}", f"{service_name}:{{name}}"
        ),  # Добавляем имя сервиса в формат
        colorize=True,
        serialize=config.serialize,
    )

    # Обработчик для записи в файл (если включено)
    if config.enable_file_logging:
        log_file_path_formatted = config.log_file_path.format(
            service_name=service_name.lower(), time="{time}"
        )
        # Убедимся, что директория logs существует
        log_dir = os.path.dirname(
            log_file_path_formatted.split("{time}")[0]
        )  # Получаем путь к директории
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                logger.warning(f"Could not create log directory {log_dir}: {e}")
                # Логирование в файл не будет работать, но консольное останется

        logger.add(
            log_file_path_formatted,
            level=config.level.upper(),
            format=config.format.replace("{name}", f"{service_name}:{{name}}"),
            rotation=config.rotation,
            retention=config.retention,
            serialize=config.serialize,
            encoding="utf-8",
        )

    # Интеграция с Sentry (если DSN указан)
    if config.sentry_dsn:
        try:
            # Опциональная зависимость, установите sentry-sdk, если используете
            import sentry_sdk
            from sentry_sdk.integrations.loguru import LoguruIntegration

            sentry_loguru_integration = LoguruIntegration(
                level=config.level.upper(),  # Уровень логов, которые отправляются как breadcrumbs
                event_level="WARNING",  # Уровень логов, которые отправляются как события Sentry
            )
            sentry_sdk.init(
                dsn=config.sentry_dsn,
                integrations=[sentry_loguru_integration],
                # Установите traces_sample_rate=1.0 для захвата 100%
                # транзакций для мониторинга производительности.
                # Мы рекомендуем настроить это значение в продакшене.
                traces_sample_rate=1.0,  # Можно сделать настраиваемым
                # Если вы хотите передавать PII (Personally Identifiable Information) в Sentry
                # send_default_pii=True
                environment=os.getenv(
                    "ENVIRONMENT", "development"
                ),  # Например: development, staging, production
                release=f"{api_settings.PROJECT_NAME if api_settings else service_name.lower()}@{api_settings.API_VERSION if api_settings else '0.1.0'}",
                # Пример релиза
            )
            logger.info(f"Sentry integration enabled for service: {service_name}")
        except ImportError:
            logger.warning(
                "Sentry DSN provided, but 'sentry-sdk' is not installed. "
                "Sentry integration will be disabled. "
                "Install with: poetry add sentry-sdk"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Sentry for service {service_name}: {e}")

    logger.info(
        f"Logger configured for service: {service_name} with level: {config.level}"
    )


# Можно экспортировать сам логгер, если хотите использовать его напрямую после настройки
# from loguru import logger as service_logger
# __all__ = ["setup_logger", "service_logger", "LogConfig"]
__all__ = ["setup_logger", "LogConfig"]
