from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Personal Finance API",
        default_version="v1",
        contact=openapi.Contact(email="felipe.carvalho07@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/auth/", include("authy.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/transactions/", include("transactions.urls")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
]
