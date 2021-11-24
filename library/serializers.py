from rest_framework import serializers
from library.models import Plant, Image


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = (
            "id",
            "slug",
            "latin_name",
            "family",
            "food_text",
            "description",
            "medicinal_uses",
            "warnings",
            "poisonous_look_alike",
            "trees",
            "shrubs",
            "lichens",
            "herbs",
            "poisonous",
            "in_colorado",
            "in_idaho",
            "in_montana",
            "in_new_mexico",
            "in_utah",
            "in_washington",
            "in_wyoming",
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "plant",
            "image_author",
            "image_link",
            "license",
            "image",
        )
