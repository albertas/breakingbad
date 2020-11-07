from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Breaking Bad API",
        default_version="v1",
        description="API for Breaking Bad character investigation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
]
