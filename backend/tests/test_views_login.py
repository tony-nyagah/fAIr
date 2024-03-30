from django.test import TestCase
from rest_framework.test import APIClient

client = APIClient()

API_BASE = "http://testserver/api/v1"


class LoginViewTestCase(TestCase):
    def test_login_url_returns_200(self):
        response = client.get(f"{API_BASE}/auth/login/")
        self.assertEqual(response.status_code, 200)

    def test_response_type_is_json(self):
        response = client.get(f"{API_BASE}/auth/login/")
        self.assertEqual(response["content-type"], "application/json")

    def test_response_contains_login_url(self):
        response = client.get(f"{API_BASE}/auth/login/")
        self.assertTrue("login_url" in response.json())
