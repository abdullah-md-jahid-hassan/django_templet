from django.db import models

from emails.choices import (
    EmailBodyType,
    EmailStatus,
)

class EmailLog(models.Model):
    to_email = models.TextField()
    from_email = models.EmailField()

    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    body_type = models.CharField(max_length=255, choices=EmailBodyType.choices, default=EmailBodyType.TEXT)

    status = models.CharField(max_length=255, choices=EmailStatus.choices, default=EmailStatus.SENT)
    schedule_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)
