from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Dataset
from .serializers import DatasetSerializer
from .services import get_file_type
from .tasks import process_dataset


class DatasetViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file_type = get_file_type(serializer.validated_data["file"].name)
        dataset = serializer.save(user=self.request.user, file_type=file_type)
        process_dataset.delay(dataset.pk)
