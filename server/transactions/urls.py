from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transactions.views import TransactionViewSet

router = DefaultRouter()
router.register(
    r"",
    TransactionViewSet,
    basename="transactions",
)

urlpatterns = [
    path(r"", include(router.urls)),
]
