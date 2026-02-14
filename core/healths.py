import smtplib
import traceback
from django.conf import settings
from core.utils.health_response import health_ok_response, health_error_response
from django.db import connection

import smtplib
import traceback
from django.conf import settings

def check_email_service():
    try:
        # Choose SMTP class based on port
        if settings.EMAIL_PORT == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=5)
        else:
            # Normal connection with optional TLS
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=5)
            server.ehlo()
            server.starttls()
            server.ehlo()

        # Attempt login (force authentication)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Optional: send a NOOP to confirm server accepts commands after login
        code, message = server.noop()
        if code != 250:
            raise Exception(f"SMTP NOOP failed: {message.decode()}")

        server.quit()
        return health_ok_response(name='Email Service')

    except smtplib.SMTPAuthenticationError as auth_err:
        return health_error_response(
            name='Email Service',
            message="SMTP authentication failed",
            errors=str(auth_err),
            traceback=traceback.format_exc(),
        )
    except smtplib.SMTPException as smtp_err:
        return health_error_response(
            name='Email Service',
            message="SMTP server error",
            errors=str(smtp_err),
            traceback=traceback.format_exc(),
        )
    except Exception as e:
        return health_error_response(
            name='Email Service',
            message="Email service check failed",
            errors=str(e),
            traceback=traceback.format_exc(),
        )

def check_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()

        return health_ok_response(
            name="Database",
            message="Health OK",
        )

    except Exception as e:
        return health_error_response(
            name="Database",
            message="Health Error",
            errors=str(e),
            traceback=traceback.format_exc().splitlines(),
        )
