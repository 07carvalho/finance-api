from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from accounts.permissions import IsOwner
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
