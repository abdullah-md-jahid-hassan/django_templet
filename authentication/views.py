from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import error_response, success_response
from authentication.services.password import change_password

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle
from rest_framework import status
from authentication.serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from django.conf import settings

CONFIG = settings.CONFIG

# Register endpoint
class RegisterThrottle(AnonRateThrottle):
    scope = "register"
class ResisterView(APIView):
    throttle_classes = [RegisterThrottle]
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Register endpoint:
        - validates user data
        - creates a new user
        """
        # Validate user data
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid user data",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        # Create a new user
        user = serializer.save()

        # Obtain JWT tokens
        refresh = RefreshToken.for_user(user)

        return success_response(
            message="User registered successfully",
            data={
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status_code=status.HTTP_201_CREATED,
        )

# Strict throttle for login
class LoginThrottle(AnonRateThrottle):
    scope = "login"
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Login endpoint:
        - validates credentials
        - returns access + refresh tokens
        - protected by throttle
        """
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(
                message="Successfully logged out",
                status_code=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return error_response(
                message="Invalid token",
                errors=Exception,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        return success_response(
            message="User verified successfully",
            data={
                "id": user.id,
                "email": user.email,
            },
            status_code=status.HTTP_200_OK,
        )

class ChangePasswordThrottle(AnonRateThrottle):
    scope = "change_password"
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ChangePasswordThrottle]
    def post(self, request):
        user = request.user
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        try:
            user.check_password(old_password)
        except Exception:
            return error_response(
                message="Invalid old password",
                errors=Exception,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            change_password(user, new_password)
        except Exception as e:
            return error_response(
                message="Password change failed",
                errors=e,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


