"""Создаём экземпляр настроенного логгера для API"""

from src.api.core.config import settings
from src.core_shared.logging_setup import setup_logger

# Получаем экземпляр логгера API
api_log = setup_logger(service_name="API", log_level_override=settings.LOG_LEVEL)
