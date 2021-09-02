from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.models import Account
from authy.tests.factories import UserFactory


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    user = SubFactory(UserFactory)
    name = "New Account"
    bank = None
