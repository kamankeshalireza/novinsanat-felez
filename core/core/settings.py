"""
Django settings for core project — Liara production-ready configuration.

Environment-driven configuration: nothing sensitive is hardcoded.
For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Management commands that only need Django to *import* settings, never to
# actually serve a request. Liara (like most Docker-based PaaS) runs these
# during the image BUILD step, where panel-configured environment variables
# are not injected yet — those only become available once the container
# starts at RUNTIME. So SECRET_KEY is allowed to be missing here, but is
# still required to actually run the server (runserver/gunicorn/etc.).
_BUILD_ONLY_COMMANDS = {
    "collectstatic",
    "check",
    "makemigrations",
    "compilemessages",
    "shell",
}
_is_build_only_command = len(sys.argv) > 1 and sys.argv[1] in _BUILD_ONLY_COMMANDS


def env_bool(key, default=False):
    """Parse an environment variable as a boolean (accepts true/false/1/0/yes/no)."""
    value = os.environ.get(key)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def env_list(key, default=""):
    """Parse a comma-separated environment variable into a clean list."""
    raw = os.environ.get(key, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ------------------------------------------------------------------------------
# Core / Security
# ------------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
# Must be provided via the SECRET_KEY environment variable in Liara.
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# Defaults to False so a missing env var never accidentally exposes debug info.
DEBUG = env_bool("DEBUG", default=False)

if not SECRET_KEY:
    if DEBUG or _is_build_only_command:
        # Convenience fallback for local development and build-time management
        # commands only. Real requests are never served with this key, since
        # the real SECRET_KEY env var is injected once the container is
        # actually running (see _BUILD_ONLY_COMMANDS note above).
        SECRET_KEY = "django-insecure-build-time-placeholder-do-not-use-for-serving-requests"
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set. "
            "Set it in Liara's Environment Variables panel before deploying."
        )

# Comma-separated list of allowed hosts, e.g.:
#   ALLOWED_HOSTS=your-app.liara.run,yourdomain.com,www.yourdomain.com
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

# CSRF trusted origins must include the scheme (Django 4+), e.g.:
#   CSRF_TRUSTED_ORIGINS=https://your-app.liara.run,https://yourdomain.com
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")


# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
    "website.apps.WebsiteConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# ------------------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# Liara's PostgreSQL add-on injects POSTGRESQL_DB_* environment variables
# automatically once the database is attached to the app. See:
# https://docs.liara.ir/paas/django/how-tos/connect-to-db/postgresql/
# ------------------------------------------------------------------------------

if os.environ.get("POSTGRESQL_DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRESQL_DB_NAME"),
            "USER": os.environ.get("POSTGRESQL_DB_USER"),
            "PASSWORD": os.environ.get("POSTGRESQL_DB_PASS"),
            "HOST": os.environ.get("POSTGRESQL_DB_HOST"),
            "PORT": os.environ.get("POSTGRESQL_DB_PORT"),
            "CONN_MAX_AGE": 60,
        }
    }
else:
    # Fallback for local development only. NOTE: Liara's filesystem is ephemeral
    # on redeploy — do NOT rely on SQLite in production, attach the PostgreSQL
    # add-on and set the POSTGRESQL_DB_* env vars instead.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ------------------------------------------------------------------------------
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ------------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Asia/Tehran")

USE_I18N = True

USE_TZ = True


# ------------------------------------------------------------------------------
# Static & media files
# https://docs.djangoproject.com/en/5.2/howto/static-files/
#
# Static files are served directly by WhiteNoise (compressed + hashed +
# cached), so no external static file service is required.
# ------------------------------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ------------------------------------------------------------------------------
# File upload hardening
# ------------------------------------------------------------------------------

DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB
FILE_UPLOAD_PERMISSIONS = 0o644


# ------------------------------------------------------------------------------
# Security hardening (production)
#
# Liara terminates TLS at its edge/nginx layer and forwards requests to the
# app over HTTP with an X-Forwarded-Proto header, so we trust that header to
# detect HTTPS and force secure redirects/cookies.
# https://docs.djangoproject.com/en/5.2/topics/security/
# ------------------------------------------------------------------------------

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True

    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=True)

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

    # A session that outlives the browser tab is a smaller attack surface.
    SESSION_EXPIRE_AT_BROWSER_CLOSE = env_bool("SESSION_EXPIRE_AT_BROWSER_CLOSE", default=False)
    SESSION_COOKIE_AGE = int(os.environ.get("SESSION_COOKIE_AGE", str(60 * 60 * 24 * 14)))  # 14 days


# ------------------------------------------------------------------------------
# Logging — send everything to stdout so it shows up in Liara's log viewer.
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
