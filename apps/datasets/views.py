from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsOwner

from .models import Dataset
from .serializers import DatasetSerializer
from .services import get_file_type
from .tasks import process_dataset


class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file_type = get_file_type(serializer.validated_data["file"].name)
        dataset = serializer.save(user=self.request.user, file_type=file_type)
        process_dataset.delay(dataset.pk)
