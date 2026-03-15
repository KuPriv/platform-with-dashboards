import os

from .base import *  # noqa: F401, F403
from .base import SPECTACULAR_SETTINGS

SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-local-dev-only-do-not-use-in-production"
)
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
SPECTACULAR_SETTINGS["SERVE_INCLUDE_SCHEMA"] = False
