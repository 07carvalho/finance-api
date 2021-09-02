from datetime import datetime

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from accounts.models import Account
from accounts.permissions import IsOwner
from accounts.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, last_update=datetime.now())
