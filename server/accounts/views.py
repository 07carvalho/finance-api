from datetime import datetime

from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication

from accounts.models import Account
from accounts.permissions import IsOwner
from accounts.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(
            user=self.request.user,
        )
        if account_type := self.request.query_params.get("type"):
            queryset = queryset.filter(type=account_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, last_update=datetime.now())
