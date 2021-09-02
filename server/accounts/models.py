from datetime import datetime
from decimal import Decimal

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

    def update_values_from_new_income(self, value: Decimal):
        self.income += value
        self.balance += value

    def update_values_from_new_expense(self, value: Decimal):
        self.expense -= value
        self.balance -= value

    def manage_values_from_new_transaction(self, transaction_type: str, value: Decimal):
        transaction_adapter = {
            "in": self.update_values_from_new_income,
            "ex": self.update_values_from_new_expense,
        }
        transaction_adapter[transaction_type](value)
        self.last_update = datetime.now()
        self.save()

    def refund_income(self, value: Decimal):
        self.income -= value
        self.balance -= value

    def refund_expense(self, value: Decimal):
        self.expense += value
        self.balance += value

    def refund_values_from_deleted_transaction(
        self, transaction_type: str, value: Decimal
    ):
        transaction_adapter = {
            "in": self.refund_income,
            "ex": self.refund_expense,
        }
        transaction_adapter[transaction_type](value)
        self.last_update = datetime.now()
        self.save()

    def exchange_income(self, old_value: Decimal, new_value: Decimal):
        self.refund_income(old_value)
        self.update_values_from_new_income(new_value)

    def exchange_expense(self, old_value: Decimal, new_value: Decimal):
        self.refund_expense(old_value)
        self.update_values_from_new_expense(new_value)

    def exchange_values_from_updated_transaction(
        self, transaction_type: str, old_value: Decimal, new_value: Decimal
    ):
        transaction_adapter = {
            "in": self.exchange_income,
            "ex": self.exchange_expense,
        }
        transaction_adapter[transaction_type](old_value, new_value)
        self.last_update = datetime.now()
        self.save()
