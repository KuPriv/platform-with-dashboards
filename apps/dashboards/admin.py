from django.contrib import admin

from .models import Dashboard, Widget


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_filter = ("user",)


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ("id", "dashboard", "dataset", "chart_type")
    list_filter = ("chart_type",)
