from core.choices import OtpPurpose
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from emails.tasks import send_email_task
from emails.choices import (
    EmailBodyType,
    EmailPurpose,
)
from datetime import datetime


User = get_user_model()

def send_otp_email(
        email: str, 
        otp: str, 
        otp_porous: OtpPurpose.choices = OtpPurpose.OTHER,
        ):
    send_email_task.delay(
        subject=f"Your {otp_porous} OTP Code",
        to_emails=[email],
        body=render_to_string(
            "emails/otp_email.html",
            {
                "otp": otp,
                "porous": otp_porous,
                "current_year": datetime.now().year,
            }
        ),
        body_type=EmailBodyType.HTML,
        purpose=EmailPurpose.OTP,
    )
    


