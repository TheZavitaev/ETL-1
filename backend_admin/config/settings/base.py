import os

SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-7bb$bzyjj7*tvw!q7dlm-za3wtoxt)ka6@$-c^abi*(6s7)g"
)
DEBUG = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "movies",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


POSTGRES_SCHEMA_CONTENT_NAME = os.getenv("POSTGRES_SCHEMA_CONTENT_NAME")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=public,postgres"},
        "NAME": os.getenv("POSTGRES_DB_NAME", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "@J2JqrPRYoFnVv2jvV"),
        "CONN_MAX_AGE": 0,
    },
    "content": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"options": "-c search_path=content,postgres"},
        "NAME": os.getenv("POSTGRES_DB_NAME", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "@J2JqrPRYoFnVv2jvV"),
        "CONN_MAX_AGE": 0,
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.environ.get("STATIC_ROOT", "/static")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
        },
    },
    "handlers": {
        "debug-console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["debug-console"],
            "propagate": False,
        }
    },
}
