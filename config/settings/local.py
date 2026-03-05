import tomllib

from .base import *  # noqa: F401, F403
from .base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Письма выводятся в консоль
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# django-debug-toolbar
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",
]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
INTERNAL_IPS = ["127.0.0.1"]

# Spectacular settings
with open(BASE_DIR / "pyproject.toml", "rb") as f:
    _pyproject = tomllib.load(f)
SPECTACULAR_SETTINGS = {
    "TITLE": "Platform With Dashboards API",
    "DESCRIPTION": "REST API для загрузки датасетов и управления дашбордами",
    "VERSION": _pyproject["project"]["version"],
    "SERVE_INCLUDE_SCHEMA": False,
}
