from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication

from accounts.permissions import IsOwner
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["description"]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user,
        )
        if transaction_type := self.request.query_params.get("type"):
            queryset = queryset.filter(type=transaction_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
