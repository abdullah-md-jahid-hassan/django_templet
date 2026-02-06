from django.db.models import TextChoices

class EmailBodyType(TextChoices):
    HTML = 'html', 'HTML'
    TEXT = 'text', 'TEXT'

class EmailStatus(TextChoices):
    SENT = 'sent', 'SENT'
    FAILED = 'failed', 'FAILED'
    SCHEDULED = 'scheduled', 'SCHEDULED'
