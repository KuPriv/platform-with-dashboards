import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.datasets.models import Dataset


@pytest.fixture
def dataset(user):
    return Dataset.objects.create(
        name="Test Dataset",
        file_type="csv",
        user=user,
        file=SimpleUploadedFile(
            "test.csv", b"name,age\nEgor,22", content_type="text/csv"
        ),
        status=Dataset.Status.PENDING,
    )


@pytest.fixture
def other_dataset(other_user):
    return Dataset.objects.create(
        name="Test Dataset",
        file_type="csv",
        user=other_user,
        file=SimpleUploadedFile(
            "test.csv", b"name,age\nEgor,22", content_type="text/csv"
        ),
    )


@pytest.fixture
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="example2@example.com",
        password="testpass321",
    )
