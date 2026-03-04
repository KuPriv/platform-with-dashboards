from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import IsOwner

from .models import Dataset
from .serializers import DatasetSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)
