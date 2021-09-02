from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Account
        exclude = ["user"]
