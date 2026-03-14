from functools import partial

from django.db import transaction
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Dataset
from .serializers import DatasetSerializer
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
        dataset = serializer.save(user=self.request.user)
        transaction.on_commit(partial(process_dataset.delay, dataset.pk))
