from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from authentication.views import (
    ResisterView,
    LoginView,
    LogoutView,
    VerifyUserView,
)

urlpatterns = [
    # Main Auth
    path("register/", ResisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="jwt-logout"),

    # Get new access token using refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Verify
    path("verify/", VerifyUserView.as_view(), name="jwt-verify"),
    path("token/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    # Password
    
]

