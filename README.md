```
habit-tracker-bot/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── .dockerignore
├── .env.example                # Пример переменных окружения
├── .gitignore
├── .pre-commit-config.yaml     # Конфигурация Pre-commit
├── alembic.ini                 # Конфигурация Alembic
├── docker-compose.yml          # Docker Compose конфигурация
├── Dockerfile.api              # Dockerfile для FastAPI
├── Dockerfile.bot              # Dockerfile для Telegram бота
├── Dockerfile.scheduler        # Dockerfile для Scheduler (если отдельный)
├── pyproject.toml              # Файл Poetry
├── README.md
└── src/
    ├── api/                    # FastAPI приложение (Backend)
    │   ├── main.py             # Точка входа FastAPI
    │   ├── core/               # Конфигурация, базовые настройки
    │   │   └── config.py       # Загрузка настроек (из .env)
    │   ├── db/                 # Работа с БД
    │   │   ├── models.py       # SQLAlchemy модели
    │   │   └── session.py      # Настройка асинхронной сессии
    │   ├── schemas/            # Pydantic схемы (DTO)
    │   │   └── habit.py
    │   │   └── user.py
    │   ├── services/           # Бизнес-логика (CRUD операции)
    │   │   └── habit_service.py
    │   │   └── user_service.py
    │   ├── endpoints/          # API роутеры
    │   │   └── habits.py
    │   │   └── users.py        # (Если нужна регистрация пользователя в API)
    │   └── security/           # Аутентификация/Авторизация
    │       └── auth.py         # Логика токенов, проверка API ключа бота
    ├── bot/                    # Telegram бот (Frontend)
    │   ├── main.py             # Точка входа бота
    │   ├── handlers/           # Обработчики команд и сообщений
    │   │   └── common.py
    │   │   └── habits.py
    │   ├── keyboards/          # Генерация клавиатур
    │   │   └── inline.py
    │   ├── states/             # Состояния для диалогов (если нужно)
    │   │   └── *.py
    │   ├── core/               # Конфигурация бота
    │   │   └── config.py
    │   └── api_client.py       # Клиент для взаимодействия с FastAPI
    ├── migrations/             # Alembic миграции
    │   ├── versions/           # Файлы миграций
    │   └── env.py              # Alembic среда выполнения
    │   └── script.py.mako      # Шаблон миграций
    ├── scheduler/              # Скрипт планировщика
    │   ├── main.py             # Точка входа планировщика
    │   ├── jobs.py             # Задачи для выполнения (напоминания, перенос)
    │   └── core/
    │       └── config.py
    └── tests/                  # Тесты
        ├── api/
        └── bot/
        └── scheduler/
```
