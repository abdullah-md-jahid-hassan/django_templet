import smtplib
import traceback
from django.conf import settings
from core.utils.health_response import health_ok_response, health_error_response

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
            errors=auth_err,
        )
    except smtplib.SMTPException as smtp_err:
        return health_error_response(
            name='Email Service',
            message="SMTP server error",
            errors=smtp_err,
        )
    except Exception as e:
        return health_error_response(
            name='Email Service',
            message="Email service check failed",
            errors=e,

        )
        
