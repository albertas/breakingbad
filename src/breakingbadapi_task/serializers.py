from rest_framework import serializers

from breakingbadapi_task.models import Character, Location


class CharacterSerializer(serializers.ModelSerializer):
    occupation = serializers.SlugRelatedField(slug_field="title", many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["id", "name", "birthday", "status", "occupation"]


class LocationSerializer(serializers.ModelSerializer):
    character_name = serializers.CharField(source="character.name", read_only=True)

    class Meta:
        model = Location
        fields = ["id", "character_name", "timestamp", "point", "character"]
