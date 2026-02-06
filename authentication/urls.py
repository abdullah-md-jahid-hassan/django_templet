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
    ChangePasswordView,
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
        path("password/change/", ChangePasswordView.as_view(), name="password-change"),
        # path("password/reset/", ResetPasswordView.as_view(), name="password-reset"),        

    
]

