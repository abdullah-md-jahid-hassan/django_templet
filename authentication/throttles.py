from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterThrottle(AnonRateThrottle):
    scope = "register"


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class ChangePasswordThrottle(UserRateThrottle):
    scope = "change_password"


class ResetPasswordThrottle(AnonRateThrottle):
    scope = "reset_password"
