from unittest.mock import patch
from django.test import TestCase
from django.core import mail

from emails.choices import EmailPurpose, EmailStatus
from emails.models import EmailLog
from emails.utils.general import send_email_core
from emails.services.otp import send_otp_email


class EmailMaskingTests(TestCase):
    def test_send_email_core_with_explicit_masked_log_body(self):
        send_email_core(
            subject="Your OTP",
            to_emails=["user@example.com"],
            body="<html>Your OTP is 123456</html>",
            log_body="<html>Your OTP is ******</html>",
            purpose=EmailPurpose.OTP,
            raw_otp="123456",
        )

        log = EmailLog.objects.filter(to_emails="user@example.com").first()
        self.assertIsNotNone(log)
        self.assertIn("******", log.body)
        self.assertNotIn("123456", log.body)
        self.assertEqual(log.purpose, EmailPurpose.OTP)

    def test_send_email_core_automatic_fallback_masking(self):
        # Caller did not provide log_body, but set purpose=OTP and raw_otp="654321"
        send_email_core(
            subject="Your OTP",
            to_emails=["victim@example.com"],
            body="<html>Verification code: 654321</html>",
            purpose=EmailPurpose.OTP,
            raw_otp="654321",
        )

        log = EmailLog.objects.filter(to_emails="victim@example.com").first()
        self.assertIsNotNone(log)
        self.assertIn("******", log.body)
        self.assertNotIn("654321", log.body)

    def test_normal_email_preserves_body(self):
        send_email_core(
            subject="Welcome!",
            to_emails=["newuser@example.com"],
            body="<html>Welcome to the platform!</html>",
            purpose=EmailPurpose.WELCOME,
        )

        log = EmailLog.objects.filter(to_emails="newuser@example.com").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.body, "<html>Welcome to the platform!</html>")
        self.assertEqual(log.purpose, EmailPurpose.WELCOME)
