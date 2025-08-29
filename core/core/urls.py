from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Redirects
    path("",        lambda r: redirect("/swagger/", permanent=False)),
    path("api/",    lambda r: redirect("/swagger/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # Auth / Accounts (WICHTIG: in accounts/urls KEIN weiteres 'auth/' voranstellen)
    path("api/auth/", include("accounts.urls")),

    # Django built-in auth views (optional für Login-Templates etc.)
    path("accounts/", include("django.contrib.auth.urls")),

    # JWT (separat nutzbar; kollidiert nicht mit accounts/urls)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # API-Module
    path("api/products/", include("products.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/categories/", include("categories.urls")),

    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/articles/", include("articles.urls")),  # <— hinzufügen
]

# Media/Static nur im DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)