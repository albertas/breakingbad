from django.http import HttpResponseRedirect
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework import viewsets

from breakingbadapi_task.filters import (CharacterFilter,
                                         CharacterOrderingFilter,
                                         LocationFilter)
from breakingbadapi_task.models import Character, Location
from breakingbadapi_task.serializers import (CharacterSerializer,
                                             LocationSerializer)


def index(request):
    return HttpResponseRedirect(reverse("swagger"))


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend, CharacterOrderingFilter)
    filterset_class = CharacterFilter


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter
