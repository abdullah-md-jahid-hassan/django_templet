from unittest.mock import patch
from django.test import TestCase

from emails.choices import EmailPurpose
from emails.models import EmailLog
from emails.utils.general import send_email_core
from emails.services.otp import send_otp_email


class EmailMaskingTests(TestCase):
    def test_send_email_core_with_log_body_stores_masked_content(self):
        send_email_core(
            subject="Your OTP",
            to_emails=["user@example.com"],
            body="<html>Your OTP is 123456</html>",
            log_body="<html>Your OTP is ******</html>",
            purpose=EmailPurpose.OTP,
        )

        log = EmailLog.objects.filter(to_emails="user@example.com").first()
        self.assertIsNotNone(log)
        self.assertIn("******", log.body)
        self.assertNotIn("123456", log.body)
        self.assertEqual(log.purpose, EmailPurpose.OTP)

    def test_send_email_core_without_log_body_stores_original_body(self):
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

    @patch("emails.services.otp.send_email_task.delay")
    def test_send_otp_email_passes_masked_log_body(self, mock_delay):
        send_otp_email(email="test@example.com", otp="987654")

        mock_delay.assert_called_once()
        kwargs = mock_delay.call_args.kwargs
        self.assertIn("987654", kwargs["body"])
        self.assertIn("******", kwargs["log_body"])
        self.assertNotIn("987654", kwargs["log_body"])
