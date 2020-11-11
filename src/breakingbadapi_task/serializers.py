from rest_framework import serializers

from breakingbadapi_task.models import Character, Location


class CharacterSerializer(serializers.ModelSerializer):
    occupation = serializers.SlugRelatedField(slug_field="title", many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["id", "name", "birthday", "status", "occupation"]


class LocationSerializer(serializers.ModelSerializer):
    character_name = serializers.CharField(source="character.name", read_only=True)
    point = serializers.CharField(
        help_text="Latitude and longitude of a point separated by a comma, e.g. 2.0,2.0"
    )

    def validate_point(self, value):
        if "SRID=" not in value:
            try:
                lat, lon = value.split(",")
                return f"SRID=4326;POINT ({lat.strip()} {lon.strip()})"
            except ValueError:
                message = "Could not parse latitude and longitude, please use comma to separate the values."
                serializers.ValidationError(message)
        return value

    class Meta:
        model = Location
        fields = ["id", "character_name", "timestamp", "point", "character"]
