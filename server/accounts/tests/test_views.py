import freezegun
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import Account
from accounts.tests.factories import AccountFactory
from authy.tests.factories import TokenFactory, UserFactory


class AccountTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.user_account = AccountFactory(user=self.user)
        token = TokenFactory(user=self.user).key
        self.header = {"HTTP_AUTHORIZATION": f"Token {token}"}

        another_user = UserFactory()
        self.another_account = AccountFactory(user=another_user)

    def test_list_accounts(self):
        url = reverse("accounts-list")

        response = self.client.get(url, format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["count"], Account.objects.filter(user=self.user).count()
        )

    def test_search_account(self):
        url = reverse("accounts-list")
        AccountFactory(user=self.user, name="Personal Account")
        AccountFactory(user=self.user, name="Family Account")
        AccountFactory(user=self.user, name="Savings Account")

        response = self.client.get(url + "?search=family", format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_filter_account_by_type(self):
        url = reverse("accounts-list")
        AccountFactory(user=self.user, type="cash")
        AccountFactory(user=self.user, type="cash")
        AccountFactory(user=self.user)

        response = self.client.get(url + "?type=cash", format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_search_and_filter_account_by_type(self):
        url = reverse("accounts-list")
        AccountFactory(user=self.user, name="Personal Account", type="cash")
        AccountFactory(user=self.user, name="Family Account", type="cash")
        AccountFactory(user=self.user, name="Savings Account")

        response = self.client.get(
            url + "?type=cash&search=Savings", format="json", **self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_create_account(self):
        url = reverse("accounts-list")
        payload = {
            "name": "My New Account",
            "type": "bank",
            "bank": "Big Bank",
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "My New Account")
        self.assertEqual(Account.objects.filter(user=self.user).count(), 2)

    def test_create_account_without_name(self):
        url = reverse("accounts-list")
        payload = {
            "type": "bank",
            "bank": "Big Bank",
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())
        self.assertEqual(Account.objects.filter(user=self.user).count(), 1)

    def test_retrieve_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.user_account.id})

        response = self.client.get(url, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], account.name)

    def test_retrieve_another_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.another_account.id})

        response = self.client.get(url, format="json", **self.header)

        self.assertEqual(response.status_code, 404)

    @freezegun.freeze_time("2021-09-01 13:00:00")
    def test_update_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.user_account.id})
        payload = {"name": "My Newest Account"}

        response = self.client.patch(url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], account.name)
        self.assertIsNotNone(response.json()["last_update"])
        self.assertEqual(response.json()["last_update"], "2021-09-01T13:00:00Z")

    def test_update_another_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.another_account.id})
        payload = {"name": "My Newest Account"}

        response = self.client.patch(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 404)

    def test_delete_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.user_account.id})

        response = self.client.delete(url, format="json", **self.header)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Account.objects.filter(user=self.user).count(), 0)
        self.assertEqual(Account.deleted.filter(user=self.user).count(), 1)

    def test_delete_another_account(self):
        url = reverse("accounts-detail", kwargs={"pk": self.another_account.id})

        response = self.client.delete(url, format="json", **self.header)

        self.assertEqual(response.status_code, 404)
