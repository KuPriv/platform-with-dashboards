from django.conf import settings
from rest_framework import serializers

from .models import Dataset
from .services import (
    SUPPORTED_EXTENSIONS,
    get_file_extension,
    get_file_type,
)


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "name", "file", "file_type", "status"]
        read_only_fields = ["file_type", "status"]

    def validate_file(self, value):
        if value.size > settings.MAX_DATASET_UPLOAD_SIZE:
            raise serializers.ValidationError(
                f"Размер файла не должен превышать "
                f"{settings.MAX_DATASET_UPLOAD_SIZE // 1024 // 1024}MB"
            )
        ext = get_file_extension(value.name)
        if ext not in SUPPORTED_EXTENSIONS:
            raise serializers.ValidationError("Поддерживаются только CSV и Excel файлы")
        return value

    def create(self, validated_data):
        validated_data["file_type"] = get_file_type(validated_data["file"].name)
        return super().create(validated_data)
