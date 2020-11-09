from rest_framework import serializers

from breakingbadapi_task.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    occupation = serializers.SlugRelatedField(slug_field="title", many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["id", "name", "birthday", "status", "occupation"]
