from decouple import config

class EnvConfig:
    # Security Environment Variables
    DEBUG = config('DEBUG', default=False, cast=bool)
    SECRET_KEY = config('SECRET_KEY', cast=str)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=str).split(',')

    # Login
    LOGIN_THROTTLE_RATE_PER_MINUTE = config('LOGIN_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)

    # Register
    REGISTER_THROTTLE_RATE_PER_MINUTE = config('REGISTER_THROTTLE_RATE_PER_MINUTE', default=3, cast=int)

    # Tasted Origin Settings
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=str).split(',')
    CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)

    # Email settings
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com', cast=str)
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

    # JWT settings
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES = config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=15, cast=int)
    JWT_REFRESH_TOKEN_LIFETIME_HOURS = config('JWT_REFRESH_TOKEN_LIFETIME_HOURS', default=30, cast=int)

    # Database settings
    DB_ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql', cast=str)
    DB_NAME = config('DB_NAME', cast=str)
    DB_USER = config('DB_USER', cast=str)
    DB_PASSWORD = config('DB_PASSWORD', cast=str)
    DB_HOST = config('DB_HOST', cast=str)
    DB_PORT = config('DB_PORT', default=5432, cast=int)

    # redis settings
    REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0', cast=str)

    # Celery
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0', cast=str)
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0', cast=str)
