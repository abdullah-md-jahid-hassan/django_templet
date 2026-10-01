from decouple import config

class EnvConfig:
    # Security Environment Variables
    SECRET_KEY = config('SECRET_KEY', cast=str)
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=str).split(',')

    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    NUM_PROXIES = config('NUM_PROXIES', default=1, cast=int)

    # CORS Settings
    CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)
    CORS_ALLOW_ALL_ORIGINS  = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
    if not CORS_ALLOW_ALL_ORIGINS:
        CORS_ALLOWED_ORIGINS = [origin for origin in (config('CORS_ALLOWED_ORIGINS', default='', cast=str).split(",")) if origin]
        CORS_ALLOWED_ORIGIN_REGEXES = [origin for origin in (config('CORS_ALLOWED_ORIGIN_REGEXES', default='', cast=str).split(",")) if origin]
    CSRF_TRUSTED_ORIGINS = [origin for origin in (config("CSRF_TRUSTED_ORIGINS", default="", cast=str).split(",")) if origin]
    CORS_ALLOWED_METHODS = [method for method in (config('CORS_ALLOWED_METHODS', default='', cast=str).split(",")) if method]
    if not CORS_ALLOWED_METHODS:
        CORS_ALLOWED_METHODS = [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ]
    # CORS_ALLOW_HEADERS = config('CORS_ALLOWED_ORIGINS', default='', cast=str).split(",")
    # if not CORS_ALLOW_HEADERS:
    #     CORS_ALLOW_HEADERS = [
    #         "authorization",
    #         "content-type",
    #     ]

    # Throttles Settings
    USER_THROTTLE_RATE_PER_MINUTE = config('USER_THROTTLE_RATE_PER_MINUTE', default=120, cast=int)
    ANON_THROTTLE_RATE_PER_MINUTE = config('ANON_THROTTLE_RATE_PER_MINUTE', default=20, cast=int)
    LOGIN_THROTTLE_RATE_PER_MINUTE = config('LOGIN_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)
    LOGIN_TARGET_THROTTLE_RATE_PER_MINUTE = config('LOGIN_TARGET_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)
    REGISTER_THROTTLE_RATE_PER_MINUTE = config('REGISTER_THROTTLE_RATE_PER_MINUTE', default=3, cast=int)
    CHANGE_PASSWORD_THROTTLE_RATE_PER_MINUTE = config('CHANGE_PASSWORD_THROTTLE_RATE_PER_MINUTE', default=2, cast=int)
    RESET_PASSWORD_THROTTLE_RATE_PER_MINUTE = config('RESET_PASSWORD_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)
    RESET_PASSWORD_TARGET_THROTTLE_RATE_PER_MINUTE = config('RESET_PASSWORD_TARGET_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)
    HEALTH_THROTTLE_RATE_PER_MINUTE = config('HEALTH_THROTTLE_RATE_PER_MINUTE', default=10, cast=int)
    OTP_ANON_THROTTLE_RATE_PER_MINUTE = config('OTP_ANON_THROTTLE_RATE_PER_MINUTE', default=5, cast=int)
    OTP_TARGET_THROTTLE_RATE_PER_HOUR = config('OTP_TARGET_THROTTLE_RATE_PER_HOUR', default=5, cast=int)

    # Email Settings
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com', cast=str)
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='', cast=str)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='', cast=str)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)

    # OTP
    OTP_CHANNEL=config('OTP_CHANNEL', default='email', cast=str)
    GET_OTP_THROTTLE_RATE_PER_DAY = config('GET_OTP_THROTTLE_RATE_PER_DAY', default=25, cast=int)
    OTP_LENGTH = config("OTP_LENGTH", default=6, cast=int)
    OTP_EXPIRY_MINUTES = config("OTP_EXPIRY_MINUTES", default=5, cast=int)
    OTP_ALLOW_NUMBER = config("OTP_ALLOW_NUMBER", default=True, cast=bool)
    OTP_ALLOW_CAPITAL = config("OTP_ALLOW_CAPITAL", default=False, cast=bool)
    OTP_ALLOW_SMALL = config("OTP_ALLOW_SMALL", default=False, cast=bool)
    OTP_ALLOW_SPECIAL = config("OTP_ALLOW_SPECIAL", default=False, cast=bool)
    MAX_ACTIVE_OTPS = config("MAX_ACTIVE_OTPS", default=1, cast=int)
    MAX_VERIFY_ATTEMPTS = config("MAX_VERIFY_ATTEMPTS", default=5, cast=int)

    # JWT settings
    ACCESS_TOKEN_LIFETIME_MINUTES = config('ACCESS_TOKEN_LIFETIME_MINUTES', default=15, cast=int)
    REFRESH_TOKEN_LIFETIME_HOURS = config('REFRESH_TOKEN_LIFETIME_HOURS', default=720, cast=int)

    # Database settings
    DB_ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql', cast=str)
    DB_NAME = config('DB_NAME', default='', cast=str)
    DB_USER = config('DB_USER', default='', cast=str)
    DB_PASSWORD = config('DB_PASSWORD', default='', cast=str)
    DB_HOST = config('DB_HOST', default='', cast=str)
    DB_PORT = config('DB_PORT', default=5432, cast=int)

    # redis settings
    REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0', cast=str)

    # Celery
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0', cast=str)
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0', cast=str)
    
