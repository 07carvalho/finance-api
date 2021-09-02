from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from accounts.permissions import IsOwner
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
