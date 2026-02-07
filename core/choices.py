from django.db.models import TextChoices

class OtpPorous(TextChoices):
    OTHER = 'other', 'OTHER'
    PASSWORD_CHANGE = 'password_change', 'PASSWORD CHANGE'
    REGISTRATION = 'registration', 'REGISTRATION'
