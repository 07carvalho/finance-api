from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import AccountViewSet

router = DefaultRouter()
router.register(
    r"",
    AccountViewSet,
    basename="accounts",
)

urlpatterns = [
    path(r"", include(router.urls)),
]
