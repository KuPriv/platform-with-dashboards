# Platform With Dashboards

> Аналитическая платформа с настраиваемыми дашбордами

![CI](https://gist.githubusercontent.com/KuPriv/10addf2357a528180330d3f6db745d43/raw/92831f8ab4fb1ab32eba7f10954559f0f73ee4f8/git-actions.svg)
![Coverage](https://gist.githubusercontent.com/KuPriv/2c62f8e2753c047ffcace254e68163a8/raw/a4ee2383243ea9b280c4e9c3c3e9b3faefb75a55/coverage.svg)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-6.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## О проекте

REST API платформа для загрузки данных (CSV/Excel) и их визуализации
через настраиваемые дашборды. Поддерживает ролевую модель пользователей
и асинхронную обработку файлов через Celery.

## Стек технологий

| Категория | Технологии |
|-----------|-----------|
| Backend | Python 3.13, Django 6.0, DRF |
| База данных | PostgreSQL, Redis |
| Очереди | Celery + Redis |
| Авторизация | JWT (SimpleJWT) |
| Линтеры | ruff, black |
| Тесты | pytest-django, coverage |
| DevOps | Docker, GitHub Actions, Nginx |

## Быстрый старт

### Требования
- Python 3.13+
- PostgreSQL 16+
- Redis 7+
- Poetry 2.0+

### Установка
```bash
git clone https://github.com/KuPriv/platformwithdashboards.git
cd platformwithdashboards

poetry install
cp .env.example .env
# заполнить .env своими значениями

poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Тесты
```bash
poetry run coverage run -m pytest -q
poetry run coverage report
```

## Архитектура
```
platformwithdashboards/
├── apps/
│   ├── users/        # JWT-аутентификация, роли
│   ├── datasets/     # Загрузка CSV/Excel, Celery-задачи
│   ├── dashboards/   # Дашборды и графики
│   └── notifications/# Email-уведомления
├── config/           # Django настройки (base/local/production)
└── services/         # Бизнес-логика
```

## Функциональность

- [x] Настройка проекта и CI/CD
- [ ] JWT аутентификация и роли пользователей
- [ ] Загрузка и парсинг CSV/Excel файлов
- [ ] Настраиваемые дашборды с графиками
- [ ] Экспорт в PDF/Excel
- [ ] Email-алерты при пороговых значениях
- [ ] Docker-деплой с Nginx

## Лицензия

MIT © [KuPriv](https://github.com/KuPriv)
