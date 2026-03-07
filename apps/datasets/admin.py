from django.contrib import admin

from .models import Dataset, DatasetRow


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "file_type",
        "status",
        "user",
        "created_at",
    )
    list_filter = (
        "status",
        "file_type",
    )
    search_fields = ("name",)


@admin.register(DatasetRow)
class DatasetRowAdmin(admin.ModelAdmin):
    list_display = (
        "dataset",
        "row_index",
    )
    list_filter = ("dataset",)
