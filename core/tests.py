from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from rest_framework.test import APIClient, APITestCase

from core.throttles import AuthenticatedUserRateThrottle, TargetIdentifierRateThrottle
from core.views import HealthCheckView

User = get_user_model()


class HealthCheckThrottleTests(APITestCase):
    def test_health_check_exempt_from_throttling(self):
        client = APIClient()
        for _ in range(25):
            response = client.get("/health/")
            self.assertEqual(response.status_code, 200)


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}})
class CoreThrottlesUnitTests(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.factory = RequestFactory()

    def test_authenticated_user_throttle_bypasses_anonymous(self):
        throttle = AuthenticatedUserRateThrottle()
        request = self.factory.get("/")
        # Anonymous request -> user is AnonymousUser
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        cache_key = throttle.get_cache_key(request, None)
        self.assertIsNone(cache_key)

    def test_authenticated_user_throttle_keys_authenticated_user(self):
        throttle = AuthenticatedUserRateThrottle()
        user = User.objects.create_user(email="auth_user@example.com", password="Password123!")
        request = self.factory.get("/")
        request.user = user
        cache_key = throttle.get_cache_key(request, None)
        self.assertIsNotNone(cache_key)
        self.assertIn(str(user.pk), cache_key)

    def test_target_identifier_throttle_extracts_and_normalizes_data(self):
        throttle = TargetIdentifierRateThrottle()
        request = self.factory.post("/", {"email": "  Victim@Example.COM  "}, content_type="application/json")
        request.data = {"email": "  Victim@Example.COM  "}
        request.user = None
        cache_key = throttle.get_cache_key(request, None)
        self.assertIsNotNone(cache_key)
        self.assertIn("victim@example.com", cache_key)
