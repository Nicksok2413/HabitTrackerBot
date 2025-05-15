"""Централизованная настройка логирования для всех сервисов проекта."""

import os
import sys

from loguru import logger
from pydantic import BaseModel, Field


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


def setup_logger(
    service_name: str,
    log_config: LogConfig | None = None,
    log_level_override: str | None = None,
) -> None:
    """
    Настраивает Loguru логгер для указанного сервиса.

    Args:
        service_name: Имя сервиса (например, "API", "Bot", "Scheduler").
        log_config: Объект конфигурации LogConfig. Если None, используются значения по умолчанию.
        log_level_override: Переопределяет уровень логирования из конфигурации.
    """
    if log_config is None:
        config = LogConfig()
    else:
        config = log_config

    # Применяем переопределения, если они есть
    if log_level_override:
        config.level = log_level_override

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

    logger.info(
        f"Logger configured for service: {service_name} with level: {config.level}"
    )


# Можно экспортировать сам логгер, если хотите использовать его напрямую после настройки
# from loguru import logger as service_logger
# __all__ = ["setup_logger", "service_logger", "LogConfig"]
__all__ = ["setup_logger", "LogConfig"]
