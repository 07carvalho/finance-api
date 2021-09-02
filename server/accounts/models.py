from django.contrib.auth.models import User
from django.db import models
from handlers.managers import BaseModel

from accounts.managers import ActivatedAccountManager


class Account(BaseModel):
    ACCOUNT_TYPE = (
        ("bank", "Bank Account"),
        ("cash", "Cash"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False)
    type = models.CharField(
        max_length=4, choices=ACCOUNT_TYPE, default="bank", null=False, blank=False
    )
    bank = models.CharField(max_length=120, null=True, blank=True)
    income = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, null=False, blank=False
    )
    expense = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, null=False, blank=False
    )
    balance = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, null=False, blank=False
    )
    last_update = models.DateTimeField(null=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_filed = models.BooleanField(default=False)

    activated = ActivatedAccountManager()

    class Meta:
        app_label = "accounts"
        ordering = ["name"]

    def __str__(self):
        return self.name
