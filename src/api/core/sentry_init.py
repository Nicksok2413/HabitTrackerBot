"""Настройка Sentry SDK."""

from logging import INFO, ERROR

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.loguru import LoguruIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from src.api.core.config import settings
from src.core_shared.logging_setup import setup_logger
from loguru import logger as sentry_logger  # Импортируем сам логгер

# Настраиваем логгер
setup_logger(service_name="Sentry", log_level_override=settings.LOG_LEVEL)


def initialize_sentry():
    """
    Инициализирует Sentry SDK, если задан DSN.
    Определяет environment, sample rates и другие параметры на основе settings.
    """
    sentry_dsn = settings.SENTRY_DSN

    if not sentry_dsn:
        sentry_logger.warning(
            "SENTRY_DSN не установлен в .env. Sentry SDK не инициализирован."
        )
        return

    # --- Определяем параметры Sentry ---

    # Окружение (Environment)
    if settings.PRODUCTION:
        environment = "production"
    else:  # Development
        environment = "development"

    # Частота семплирования для Performance Monitoring (Traces)
    # Установим 10% для production, 100% для development
    if environment == "production":
        traces_sample_rate = 0.1
    else:
        traces_sample_rate = 1.0  # Отслеживаем все в разработке

    # Частота семплирования для Profiling
    # Аналогично трейсам, или можно задать другие значения
    if environment == "production":
        profiles_sample_rate = 0.1
    else:
        profiles_sample_rate = 1.0

    # Уровни логирования для интеграции
    log_level_breadcrumbs = INFO  # Уровень для breadcrumbs
    log_level_events = ERROR  # Уровень для событий/ошибок

    sentry_logger.info(
        f"Инициализация Sentry SDK. DSN: {'***' + sentry_dsn[-6:]}, "
        f"Environment: {environment}, "
        f"Traces Rate: {traces_sample_rate}, "
        f"Profiles Rate: {profiles_sample_rate}"
    )

    try:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                StarletteIntegration(transaction_style="endpoint"),
                FastApiIntegration(transaction_style="endpoint"),
                SqlalchemyIntegration(),
                LoguruIntegration(
                    level=log_level_breadcrumbs, event_level=log_level_events
                ),
            ],
            environment=environment,
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            release=f"{settings.PROJECT_NAME}@{settings.API_VERSION}",
        )
        sentry_logger.info("Sentry SDK успешно инициализирован.")
    except Exception as exc:
        sentry_logger.exception(f"Ошибка инициализации Sentry SDK: {exc}")
