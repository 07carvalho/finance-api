from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authy.tests.factories import TokenFactory, UserFactory
from categories.models import Category
from categories.tests.factories import CategoryFactory


class CategoryTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.user_category = CategoryFactory(user=self.user)
        token = TokenFactory(user=self.user).key
        self.header = {"HTTP_AUTHORIZATION": f"Token {token}"}

        another_user = UserFactory()
        self.another_category = CategoryFactory(user=another_user)

    def test_list_categories(self):
        url = reverse("categories-list")

        response = self.client.get(url, format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["count"], Category.objects.filter(user=self.user).count()
        )

    def test_create_category(self):
        url = reverse("categories-list")
        payload = {
            "name": "My New Category",
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "My New Category")
        self.assertEqual(Category.objects.filter(user=self.user).count(), 2)

    def test_create_category_with_empty_name(self):
        url = reverse("categories-list")
        payload = {
            "name": "",
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())
        self.assertEqual(Category.objects.filter(user=self.user).count(), 1)

    def test_retrieve_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.user_category.id})

        response = self.client.get(url, format="json", **self.header)
        category = Category.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], category.name)

    def test_retrieve_another_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.another_category.id})

        response = self.client.get(url, format="json", **self.header)

        self.assertEqual(response.status_code, 404)

    def test_update_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.user_category.id})
        payload = {"name": "My Newest Category"}

        response = self.client.patch(url, data=payload, format="json", **self.header)
        category = Category.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], category.name)

    def test_update_another_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.another_category.id})
        payload = {"name": "My Newest Category"}

        response = self.client.patch(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 404)

    def test_delete_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.user_category.id})

        response = self.client.delete(url, format="json", **self.header)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.filter(user=self.user).count(), 0)
        self.assertEqual(Category.deleted.filter(user=self.user).count(), 1)

    def test_delete_another_category(self):
        url = reverse("categories-detail", kwargs={"pk": self.another_category.id})

        response = self.client.delete(url, format="json", **self.header)

        self.assertEqual(response.status_code, 404)
