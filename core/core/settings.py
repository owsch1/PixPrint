# core/core/settings.py
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# -------------------------------------------------
# Pfade & .env
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# .env liegt eine Ebene über manage.py (also /home/owsch/PixPrint/.env)
load_dotenv(BASE_DIR.parent / ".env")

def _csv(name: str, default: str = "") -> list[str]:
    val = os.getenv(name, default)
    return [p.strip() for p in val.split(",") if p.strip()]

# -------------------------------------------------
# Sicherheit & Basis
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only")  # niemals so in Produktion!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = _csv(
    "ALLOWED_HOSTS",
    "owsch.pythonanywhere.com,127.0.0.1,localhost"
)

CSRF_TRUSTED_ORIGINS = _csv(
    "CSRF_TRUSTED_ORIGINS",
    "https://owsch.pythonanywhere.com,https://*.pythonanywhere.com,"
    "http://localhost:5173,http://localhost:3000"
)

# Hinter Proxy/HTTPS (PythonAnywhere)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------
# Apps
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # extern
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "django_filters",
    "corsheaders",

    # intern
    "accounts",
    "products",
    "orders",
    "categories",
    "articles",
]

# -------------------------------------------------
# Middleware (CORS muss vor CommonMiddleware stehen)
# -------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
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

# -------------------------------------------------
# Datenbank (Standard: SQLite, via .env umstellbar)
# -------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
    }
}

# -------------------------------------------------
# Auth / i18n
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Bishkek"  # deine Lokalzeit
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = "accounts.User"

# -------------------------------------------------
# Static & Media
# -------------------------------------------------
# Auf PA: STATIC_ROOT wird per collectstatic befüllt und im Web-Tab gemappt
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Eigene statische Quellen (optional)
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------
# DRF & JWT
# -------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -------------------------------------------------
# Swagger / OpenAPI
# -------------------------------------------------
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

# -------------------------------------------------
# CORS
# -------------------------------------------------
CORS_ALLOWED_ORIGINS = _csv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
    "content-type",
]
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
# Nur API-Routen
CORS_URLS_REGEX = r"^/api/.*$"

# Cookies für Cross-Site (nur wenn du wirklich Cookies/credentials brauchst)
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE   = "None"
SESSION_COOKIE_SECURE  = True
CSRF_COOKIE_SECURE     = True