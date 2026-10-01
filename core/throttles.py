from rest_framework.throttling import AnonRateThrottle


class HealthThrottle(AnonRateThrottle):
    scope = "health"
