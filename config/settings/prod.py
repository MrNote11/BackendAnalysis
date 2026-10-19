"""
Production settings on top of base.py: hosts, CORS and CSRF origins from the environment, WhiteNoise
for static files, secure cookies and HTTPS headers.
"""
from .base import *  # noqa

# ========================
# Production Environment
# ========================
ENVIRONMENT = "prod"

# Production never runs in debug mode, whatever the environment says.
if env_bool("DEBUG", False):
    raise ValueError("DEBUG must be False in production!")
DEBUG = False

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS environment variable is not set!")

# Production must use TimescaleDB, never the SQLite fallback.
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")
DATABASES["default"]["OPTIONS"] = {
    "sslmode": "require" if env_bool("DATABASE_SSL_REQUIRE", True) else "prefer",
}

# Static files settings (using WhiteNoise)
STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", str(BASE_DIR / "staticfiles"))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
MIDDLEWARE.insert(MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa

# CORS Settings
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True

# CSRF Protection
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {module} {thread:d} - {message}",
            "style": "{",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "backend_analysis.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 14,  # Keep two weeks of logs
            "formatter": "verbose",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# =============================================================================
#       SECURITY HARDENING SETTINGS
# =============================================================================

# HTTPS/SSL Settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Cookie Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"

# Browser security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Session Security
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
