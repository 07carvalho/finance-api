from rest_framework import exceptions, serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = [
            "user",
            "deleted_at",
        ]

    def validate_value(self, value):
        if value <= 0:
            raise exceptions.ValidationError(detail="Value must be higher then zero.")
        return value
