from parameterized import parameterized
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import Account
from accounts.tests.factories import AccountFactory
from authy.tests.factories import TokenFactory, UserFactory
from categories.tests.factories import CategoryFactory
from transactions.models import Transaction
from transactions.tests.factories import TransactionFactory


class TransactionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.account = AccountFactory(user=self.user)
        self.category = CategoryFactory(user=self.user)
        self.transaction = TransactionFactory(
            user=self.user, account=self.account, category=self.category
        )
        token = TokenFactory(user=self.user).key
        self.header = {"HTTP_AUTHORIZATION": f"Token {token}"}

        self.another_user = UserFactory()
        self.another_account = AccountFactory(user=self.another_user)
        self.another_category = CategoryFactory(user=self.another_user)
        self.another_transaction = TransactionFactory(
            user=self.another_user,
            account=self.another_account,
            category=self.another_category,
        )

    def test_list_transactions(self):
        url = reverse("transactions-list")

        response = self.client.get(url, format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["count"], Transaction.objects.filter(user=self.user).count()
        )

    def test_search_transaction(self):
        url = reverse("transactions-list")
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Dinner",
        )
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Bonus",
        )
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Bonus",
        )

        response = self.client.get(url + "?search=bonus", format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_transaction_by_type(self):
        url = reverse("transactions-list")
        TransactionFactory(
            user=self.user, account=self.account, category=self.category, type="ex"
        )
        TransactionFactory(
            user=self.user, account=self.account, category=self.category, type="ex"
        )
        TransactionFactory(
            user=self.user, account=self.account, category=self.category, type="in"
        )

        response = self.client.get(url + "?type=ex", format="json", **self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_search_and_filter_transaction(self):
        url = reverse("transactions-list")
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Lunch",
            type="ex",
        )
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Salary",
            type="ex",
        )
        TransactionFactory(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Market",
            type="ex",
        )

        response = self.client.get(
            url + "?search=Mark&type=ex", format="json", **self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    @parameterized.expand(
        [
            ("ex", 23.45, "Lunch"),
            ("ex", 435.65, "Supermarket"),
            ("ex", 13.45, "Dinner"),
        ]
    )
    def test_create_expense_transaction(self, transaction_type, value, description):
        url = reverse("transactions-list")
        payload = {
            "account": self.account.id,
            "type": transaction_type,
            "description": description,
            "value": value,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], description)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(str(account.expense), "{:.2f}".format(-value))
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance - value)
        )

    @parameterized.expand(
        [
            ("in", 2000.45, "Salary"),
            ("in", 40.56, "Grandma gift"),
            ("in", 300.19, "Bonus salary"),
        ]
    )
    def test_create_income_transaction(self, transaction_type, value, description):
        url = reverse("transactions-list")
        payload = {
            "account": self.account.id,
            "type": transaction_type,
            "description": description,
            "value": value,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], description)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(str(account.income), "{:.2f}".format(self.account.income + value))
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance + value)
        )

    def test_create_transaction_equal_a_zero(self):
        url = reverse("transactions-list")
        payload = {
            "account": self.account.id,
            "type": "in",
            "description": "Bonus",
            "value": 0,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("value", response.json())

    def test_create_transaction_lower_then_zero(self):
        url = reverse("transactions-list")
        payload = {
            "account": self.account.id,
            "type": "in",
            "description": "Bonus",
            "value": -89.09,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(url, data=payload, format="json", **self.header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("value", response.json())

    def test_create_and_update_transaction(self):
        create_url = reverse("transactions-list")
        first_value = 5000
        second_value = 6000
        payload = {
            "account": self.account.id,
            "type": "in",
            "description": "Salary",
            "value": first_value,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(create_url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "Salary")
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(
            str(account.income), "{:.2f}".format(self.account.income + first_value)
        )
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance + first_value)
        )

        payload = {
            "value": second_value,
        }
        update_url = reverse("transactions-detail", kwargs={"pk": response.json()["id"]})
        response = self.client.patch(
            update_url, data=payload, format="json", **self.header
        )
        account.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Salary")
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(
            str(account.income), "{:.2f}".format(self.account.income + second_value)
        )
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance + second_value)
        )

    def test_create_and_update_transaction_with_different_type(self):
        create_url = reverse("transactions-list")
        first_value = 5000
        second_value = 6000
        payload = {
            "account": self.account.id,
            "type": "in",
            "description": "Salary",
            "value": first_value,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(create_url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "Salary")
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(
            str(account.income), "{:.2f}".format(self.account.income + first_value)
        )
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance + first_value)
        )

        payload = {
            "type": "ex",
            "value": second_value,
        }
        update_url = reverse("transactions-detail", kwargs={"pk": response.json()["id"]})
        response = self.client.patch(
            update_url, data=payload, format="json", **self.header
        )
        account.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Salary")
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(str(account.income), "{:.2f}".format(self.account.income))
        self.assertEqual(str(account.expense), "{:.2f}".format(-second_value))
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance - second_value)
        )

    def test_create_and_delete_transaction(self):
        create_url = reverse("transactions-list")
        first_value = 5000
        payload = {
            "account": self.account.id,
            "type": "in",
            "description": "Salary",
            "value": first_value,
            "date": "2021-08-31",
            "category": self.category.id,
        }

        response = self.client.post(create_url, data=payload, format="json", **self.header)
        account = Account.objects.get(user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["description"], "Salary")
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
        self.assertEqual(
            str(account.income), "{:.2f}".format(self.account.income + first_value)
        )
        self.assertEqual(
            str(account.balance), "{:.2f}".format(self.account.balance + first_value)
        )

        update_url = reverse("transactions-detail", kwargs={"pk": response.json()["id"]})
        response = self.client.delete(update_url, format="json", **self.header)
        account.refresh_from_db()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 1)
        self.assertEqual(str(account.income), str(self.account.income))
        self.assertEqual(str(account.balance), str(self.account.balance))
