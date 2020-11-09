from rest_framework import viewsets

from breakingbadapi_task.models import Character
from breakingbadapi_task.serializers import CharacterSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
