from rest_framework import serializers

from services.dataset_utils import get_file_type

from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "name", "file", "file_type", "status"]
        read_only_fields = ["file_type", "status"]

    def validate_file(self, value):
        ext = value.name.split(".")[-1].lower()
        if ext not in ["csv", "xlsx", "xls", "xlsm"]:
            raise serializers.ValidationError("Поддерживаются только CSV и Excel файлы")
        return value

    def create(self, validated_data):
        file_type = get_file_type(validated_data["file"].name)
        validated_data["file_type"] = file_type
        validated_data["user"] = self.context["request"].user
        return Dataset.objects.create(**validated_data)
