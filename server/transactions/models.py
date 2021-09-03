from django.contrib.auth.models import User
from django.db import models
from handlers.managers import BaseModel

from accounts.models import Account
from accounts.services import AccountService
from categories.models import Category


class Transaction(BaseModel):
    EXPENSE = "ex"
    INCOME = "in"
    TRANSACTION_TYPE = (
        (EXPENSE, "Expense"),
        (INCOME, "Income"),
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
        account = AccountService(account=self.account)
        if self._state.adding:
            account.manage_values_from_new_transaction(self.type, self.value)
        else:
            transaction = Transaction.objects.get(pk=self.pk)
            if self.type == transaction.type:
                account.exchange_values_from_updated_transaction(
                    self.type, transaction.value, self.value
                )
            elif self.type == self.EXPENSE:
                account.refund_income_and_update_expense(transaction.value, self.value)
            elif self.type == self.INCOME:
                account.refund_expense_and_update_income(transaction.value, self.value)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        account = AccountService(account=self.account)
        account.refund_values_from_deleted_transaction(self.type, self.value)
        return super().delete(*args, **kwargs)
