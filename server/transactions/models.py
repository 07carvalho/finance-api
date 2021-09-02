from django.contrib.auth.models import User
from django.db import models
from handlers.managers import BaseModel

from accounts.models import Account
from categories.models import Category


class Transaction(BaseModel):
    TRANSACTION_TYPE = (
        ("in", "Income"),
        ("ex", "Expense"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2, choices=TRANSACTION_TYPE, null=False, blank=False
    )
    description = models.CharField(max_length=120, null=False, blank=False)
    value = models.DecimalField(max_digits=9, decimal_places=2, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    class Meta:
        app_label = "transactions"
        ordering = ["description"]

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.account.manage_values_from_new_transaction(self.type, self.value)
        else:
            transaction = Transaction.objects.get(pk=self.pk)
            self.account.exchange_values_from_updated_transaction(
                self.type, transaction.value, self.value
            )
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account.refund_values_from_deleted_transaction(self.type, self.value)
        return super().delete(*args, **kwargs)
