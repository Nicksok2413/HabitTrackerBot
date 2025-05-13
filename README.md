```
habit-tracker-bot/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD
│
├── migrations/                     # Alembic миграции
│   ├── versions/                   # Файлы миграций
│   ├── env.py                      # Alembic среда выполнения
│   └── script.py.mako              # Шаблон миграций
│
├── src/
│   ├── api/                        # FastAPI приложение (Backend)
│   │   ├── core/                   # Ядро (конфигурация, БД, безопасность, исключения, логирование, настройки sentry)
│   │   │   ├── config.py           # Загрузка настроек (из .env)
│   │   │   ├── database.py         # Настройка подключения к базе данных с использованием SQLAlchemy.
│   │   │   ├── exceptions.py       # Модуль кастомных исключений и их обработчиков для FastAPI.
│   │   │   ├── logging.py          # Настройка конфигурации логирования для приложения с использованием Loguru.
│   │   │   ├── security.py         # Аутентификация/Авторизация (логика токенов, проверка API ключа бота).
│   │   │   └── sentry.py           # Настройка Sentry SDK.
│   │   ├── models/                 # Модели SQLAlchemy
│   │   │   ├── base.py
│   │   │   ├── habit.py
│   │   │   └── user.py
│   │   ├── repositories/           # Репозитории (слой доступа к данным)
│   │   │   ├── base.py
│   │   │   ├── habit.py
│   │   │   └── user.py
│   │   ├── routes/                 # API слой (роуты)
│   │   │   ├── habits.py
│   │   │   └── users.py
│   │   ├── schemas/                # Схемы Pydantic (валидация)
│   │   │   ├── base.py
│   │   │   ├── habit.py
│   │   │   └── user.py
│   │   ├── services/               # Сервисы (бизнес-логика)
│   │   │   ├── base_service.py
│   │   │   ├── habit_service.py
│   │   │   └── user_service.py
│   │   └── main.py                 # Точка входа FastAPI
│   │
│   ├── bot/                        # Telegram бот (Frontend)
│   │   ├── core/                   # Конфигурация бота
│   │   │   └── config.py
│   │   ├── handlers/               # Обработчики команд и сообщений
│   │   │   ├── common.py
│   │   │   └── habits.py
│   │   ├── keyboards/              # Генерация клавиатур
│   │   │   └── inline.py
│   │   ├── states/                 # Состояния для диалогов
│   │   │   └── *.py
│   │   ├── api_client.py           # Клиент для взаимодействия с FastAPI
│   │   └── main.py                 # Точка входа бота
│   │
│   ├── scheduler/                  # Сервис планировщика
│   │   ├── core/
│   │   │   └── config.py           # Конфигурация планировщика
│   │   ├── jobs.py                 # Задачи для выполнения (напоминания, перенос)
│   │   └── main.py                 # Точка входа планировщика
│   │
│   └── tests/                      # Тесты
│       ├── api/
│       ├── bot/
│       └── scheduler/
│
├── .dockerignore                   # Игнорируемые файлы Docker при сборке
├── .env.example                    # Шаблон файла переменных окружения
├── .gitignore                      # Игнорируемые файлы Git
├── .env.example                    # Пример переменных окружения
├── .pre-commit-config.yaml         # Конфигурация Pre-commit
├── alembic.ini                     # Конфигурация Alembic
├── docker-compose.yml              # Docker Compose конфигурация (основной оркестратор)
├── Dockerfile.api                  # Dockerfile для FastAPI
├── Dockerfile.bot                  # Dockerfile для Telegram бота
├── Dockerfile.scheduler            # Dockerfile для Scheduler (если отдельный)
├── pyproject.toml                  # Файл Poetry
├── README.md                       # Этот файл
```
