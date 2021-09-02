from django.urls import include, path
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet

router = DefaultRouter()
router.register(
    r"",
    CategoryViewSet,
    basename="categories",
)

urlpatterns = [
    path(r"", include(router.urls)),
]
