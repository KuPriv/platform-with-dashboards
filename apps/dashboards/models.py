from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.datasets.models import Dataset


class Dashboard(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dashboards"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Дашборд"
        verbose_name_plural = "Дашборды"
        ordering = ["-created_at"]


class Widget(BaseModel):
    class ChartType(models.TextChoices):
        BAR = "bar", "Столбчатая"
        LINE = "line", "Линейная"
        PIE = "pie", "Круговая"
        TABLE = "table", "Таблица"

    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="widgets"
    )
    dataset = models.ForeignKey(
        Dataset, on_delete=models.PROTECT, related_name="widgets"
    )
    chart_type = models.CharField(max_length=20, choices=ChartType)
    x_column = models.CharField(max_length=100)
    y_column = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_chart_type_display()} / {self.dashboard.name}"

    class Meta:
        verbose_name = "Виджет"
        verbose_name_plural = "Виджеты"
        ordering = ["-created_at"]
