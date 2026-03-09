from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Dashboard, Widget
from .serializers import (
    DashboardSerializer,
    WidgetReadSerializer,
    WidgetWriteSerializer,
)
from .services import get_widget_chart_data


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dashboard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WidgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Widget.objects.filter(
            dashboard_id=self.kwargs["dashboard_pk"], dashboard__user=self.request.user
        ).select_related("dataset", "dashboard")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return WidgetWriteSerializer
        return WidgetReadSerializer

    def perform_create(self, serializer):
        dashboard = get_object_or_404(
            Dashboard, pk=self.kwargs["dashboard_pk"], user=self.request.user
        )
        serializer.save(dashboard=dashboard)

    @action(detail=True, methods=["get"])
    def data(self, request, pk=None, dashboard_pk=None):
        widget = get_object_or_404(
            Widget,
            pk=pk,
            dashboard_id=self.kwargs["dashboard_pk"],
            dashboard__user=request.user,
        )
        chart_data = get_widget_chart_data(widget)
        return Response(chart_data)
