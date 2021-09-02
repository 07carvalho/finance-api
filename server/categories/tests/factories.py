from factory import SubFactory
from factory.django import DjangoModelFactory

from authy.tests.factories import UserFactory
from categories.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = SubFactory(UserFactory)
    name = "New Category"
