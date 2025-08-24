from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema
schema_view = get_schema_view(
    openapi.Info(
        title="PixPrint API",
        default_version="v1",
        description="Документация API для фотопечати (JWT авторизация)",
        contact=openapi.Contact(email="api@pixprint.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # als Tuple
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Auth/Accounts
    path("api/auth/", include("accounts.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # API-Module (Achte darauf, in den App-urls KEIN zweites Prefix zu setzen)
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/categories/", include("categories.urls")),

    # Swagger (alle Varianten)
    re_path(r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0),
         name="schema-redoc"),
]

# Media/Static nur im DEV
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # (STATICFILES_DIRS nutzt Django automatisch; STATIC_ROOT wird nur für collectstatic/Prod verwendet)