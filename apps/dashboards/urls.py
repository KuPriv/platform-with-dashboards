from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import DashboardViewSet, WidgetViewSet

router = DefaultRouter()
router.register(r"", DashboardViewSet, basename="dashboard")

widgets_router = NestedDefaultRouter(router, r"", lookup="dashboard")
widgets_router.register(r"widgets", WidgetViewSet, basename="widgets")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(widgets_router.urls)),
]
