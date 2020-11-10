from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from breakingbadapi_task import views

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
    path("api/character/", views.CharacterViewSet.as_view({"get": "list"}), name="character-list"),
    path(
        "api/character/<int:pk>/",
        views.CharacterViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="character-detail",
    ),
    path("api/location/", views.LocationViewSet.as_view({"get": "list"}), name="location-list"),
    path(
        "api/location/<int:pk>/",
        views.LocationViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="location-detail",
    ),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
]
