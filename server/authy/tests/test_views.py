from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authy.tests.factories import UserFactory


class SignupTestCase(APITestCase):
    def setUp(self) -> None:
        self.payload = {
            "email": "tests@mail.com",
            "password": "tests123",
        }
        self.url = reverse("signup")

    def test_create_signup(self):
        response = self.client.post(self.url, data=self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        self.assertEqual(User.objects.count(), 1)

    def test_wrong_password_format(self):
        self.payload["password"] = "test"

        response = self.client.post(self.url, data=self.payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.json())
        self.assertEqual(User.objects.count(), 0)

    def test_required_fields(self):
        payload = {}

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.json())
        self.assertEqual(response.json()["email"][0], "This field is required.")
        self.assertEqual(response.json()["password"][0], "This field is required.")
        self.assertEqual(User.objects.count(), 0)

    def test_signup_with_existing_email(self):
        user = UserFactory()
        self.payload["email"] = user.email

        response = self.client.post(self.url, data=self.payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.json())
        self.assertEqual(User.objects.count(), 1)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.payload = {
            "email": self.user.email,
            "password": UserFactory.password,
        }
        self.url = reverse("login")

    def test_login(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_email_required(self):
        response = self.client.post(self.url, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json())

    def test_login_invalid_password(self):
        data = {
            "email": self.user.email,
            "password": "test",
        }

        response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Email or password wrong.")

    def test_inactive_user_failure(self):
        user = User.objects.get(email=self.payload["email"])
        user.is_active = False
        user.save()

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Email or password wrong.")
