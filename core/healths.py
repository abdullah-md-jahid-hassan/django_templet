import smtplib
import traceback
from django.conf import settings
from core import health
from core.utils.health_response import health_ok_response, health_error_response

def check_email_service():
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=5) as server:
            server.noop()
        return health_ok_response(name='Email Service')
    except Exception as e:
        return health_error_response(
            name='Email Service',
            message="Email service check failed",
            errors=str(e),
            traceback=traceback.format_exc().splitlines(),
        )

def check_database():
    try:
        from django.db import connection
        connection.cursor()
        return health_ok_response(name="Database", message="Health OK")
    except Exception as e:
        return health_error_response(
            name="Database", 
            message="Health Error",
            errors=str(e),
            traceback=traceback.format_exc(),
        )
