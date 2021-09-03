from datetime import datetime
from decimal import Decimal

from accounts.models import Account


class AccountService:
    def __init__(self, account: Account):
        self.account = account

    def exchange_expense(self, old_value: Decimal, new_value: Decimal):
        self.refund_expense(old_value)
        self.update_values_from_new_expense(new_value)

    def exchange_income(self, old_value: Decimal, new_value: Decimal):
        self.refund_income(old_value)
        self.update_values_from_new_income(new_value)

    def exchange_values_from_updated_transaction(
        self, transaction_type: str, old_value: Decimal, new_value: Decimal
    ):
        transaction_adapter = {
            "in": self.exchange_income,
            "ex": self.exchange_expense,
        }
        transaction_adapter[transaction_type](old_value, new_value)
        self.account.last_update = datetime.now()
        self.account.save()

    def manage_values_from_new_transaction(self, transaction_type: str, value: Decimal):
        transaction_adapter = {
            "in": self.update_values_from_new_income,
            "ex": self.update_values_from_new_expense,
        }
        transaction_adapter[transaction_type](value)
        self.account.last_update = datetime.now()
        self.account.save()

    def refund_expense(self, value: Decimal):
        self.account.expense += value
        self.account.balance += value

    def refund_income(self, value: Decimal):
        self.account.income -= value
        self.account.balance -= value

    def refund_expense_and_update_income(self, old_value: Decimal, new_value: Decimal):
        self.refund_expense(old_value)
        self.update_values_from_new_income(new_value)
        self.account.save()

    def refund_income_and_update_expense(self, old_value: Decimal, new_value: Decimal):
        self.refund_income(old_value)
        self.update_values_from_new_expense(new_value)
        self.account.save()

    def refund_values_from_deleted_transaction(
        self, transaction_type: str, value: Decimal
    ):
        transaction_adapter = {
            "in": self.refund_income,
            "ex": self.refund_expense,
        }
        transaction_adapter[transaction_type](value)
        self.account.last_update = datetime.now()
        self.account.save()

    def update_values_from_new_expense(self, value: Decimal):
        self.account.expense -= value
        self.account.balance -= value

    def update_values_from_new_income(self, value: Decimal):
        self.account.income += value
        self.account.balance += value
