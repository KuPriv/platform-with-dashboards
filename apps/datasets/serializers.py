from rest_framework import serializers

from .models import Dataset
from .services import (
    SUPPORTED_EXTENSIONS,
    get_file_extension,
)


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "name", "file", "file_type", "status"]
        read_only_fields = ["file_type", "status"]

    def validate_file(self, value):
        ext = get_file_extension(value.name)
        if ext not in SUPPORTED_EXTENSIONS:
            raise serializers.ValidationError("Поддерживаются только CSV и Excel файлы")
        return value
