from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

def change_password(user: User, new_password: str):
    validate_password(new_password, user=user)
    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user
