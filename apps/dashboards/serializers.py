from rest_framework import serializers

from .models import Dashboard, Widget
from .services import validate_widget_data


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class WidgetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ["id", "dataset", "chart_type", "x_column", "y_column", "created_at"]
        read_only_fields = [
            "id",
            "dataset",
            "chart_type",
            "x_column",
            "y_column",
            "created_at",
        ]


class WidgetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ["id", "dataset", "chart_type", "x_column", "y_column", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        try:
            validate_widget_data(
                dataset=data["dataset"],
                x_column=data["x_column"],
                y_column=data["y_column"],
                chart_type=data["chart_type"],
                user=self.context["request"].user,
            )
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return data
