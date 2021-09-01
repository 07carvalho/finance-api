from django.contrib.auth.models import User
from factory import Sequence
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"test_email{n}@email.com")
    email = Sequence(lambda n: f"test_email{n}@email.com")
    password = "pass$123"

    @classmethod
    def _create(cls, user_class, *args, **kwargs):
        """Create an instance of the User, and save it to the database."""
        manager = cls._get_manager(user_class)
        if cls._meta.django_get_or_create:
            user = cls._get_or_create(user_class, *args, **kwargs)
        else:
            user = manager.create_user(*args, **kwargs)
        user.raw_password = cls.password
        return user
