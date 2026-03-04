from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Dataset(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        STARTED = "started", "В обработке"
        SUCCESS = "success", "Успешно"
        FAILURE = "failure", "Ошибка"

    class FileType(models.TextChoices):
        CSV = "csv", "CSV"
        EXCEL = "excel", "Excel"

    name = models.CharField(max_length=150)
    file_type = models.CharField(max_length=20, choices=FileType)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="datasets"
    )
    file = models.FileField(upload_to="datasets/")
    status = models.CharField(max_length=20, choices=Status, default=Status.PENDING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Датасет"
        verbose_name_plural = "Датасеты"


class DatasetRow(BaseModel):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="rows")
    data = models.JSONField()
    row_index = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return f"{self.dataset.name} / row {self.row_index}"

    class Meta:
        verbose_name = "Строка данных"
        verbose_name_plural = "Строки данных"
        ordering = ["row_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["dataset", "row_index"], name="unique_dataset_row"
            )
        ]
