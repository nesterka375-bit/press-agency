from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "test_password123"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login_view_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_view_post_success(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get("_auth_user_id"))

    def test_redirect_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 302)

    def test_custom_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        self.assertTrue(self.client.session.get("_auth_user_id"))
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(
            response, reverse("catalog:index"), fetch_redirect_response=False
        )
        self.assertFalse("_auth_user_id" in self.client.session)
