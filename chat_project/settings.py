"""
Django settings for chat_project project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------
# CORE SETTINGS
# -------------------------------------------------

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-key")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


ALLOWED_HOSTS = split_csv(
    os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "ntchat.azurewebsites.net",
    )
)

# Azure automatically provides WEBSITE_HOSTNAME
azure_hostname = os.getenv("WEBSITE_HOSTNAME")
if azure_hostname and azure_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(azure_hostname)

CSRF_TRUSTED_ORIGINS = split_csv(
    os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "")
)

if azure_hostname:
    CSRF_TRUSTED_ORIGINS.append(f"https://{azure_hostname}")


# -------------------------------------------------
# APPS
# -------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "accounts_app",
    "messages_app",
    "notifications_app",
    "rooms_app",
    "profiles_app",
    "staff_panel_app",
]


# -------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------

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


ROOT_URLCONF = "chat_project.urls"

WSGI_APPLICATION = "chat_project.wsgi.application"


# -------------------------------------------------
# TEMPLATES
# -------------------------------------------------

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
                "accounts_app.context_processors.current_profile",
            ],
        },
    },
]


# -------------------------------------------------
# DATABASE (AZURE POSTGRES ONLY VIA ENV VARS)
# -------------------------------------------------

conn = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")

parsed = urlparse(conn)
qs = parse_qs(parsed.query)

DATABASES = {
        "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {"sslmode": "require"},
    }
}

# -------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------
# STATIC / MEDIA
# -------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------------------------------
# SECURITY (AZURE SAFE DEFAULTS)
# -------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SECURE_SSL_REDIRECT = not DEBUG


# -------------------------------------------------
# AUTH
# -------------------------------------------------

AUTH_USER_MODEL = "accounts_app.ChatUser"

LOGIN_REDIRECT_URL = "room_list"
LOGOUT_REDIRECT_URL = "room_list"


# -------------------------------------------------
# DRF
# -------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}