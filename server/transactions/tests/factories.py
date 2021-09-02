import datetime

from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.tests.factories import AccountFactory
from authy.tests.factories import UserFactory
from categories.tests.factories import CategoryFactory
from transactions.models import Transaction


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = SubFactory(UserFactory)
    account = SubFactory(AccountFactory)
    category = SubFactory(CategoryFactory)
    type = "in"
    description = "Service"
    value = 200.99
    date = datetime.date(2021, 9, 1)
