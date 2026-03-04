from rest_framework import routers

from .views import DatasetViewSet

router = routers.DefaultRouter()
router.register(r"", DatasetViewSet, basename="datasets")

urlpatterns = router.urls
