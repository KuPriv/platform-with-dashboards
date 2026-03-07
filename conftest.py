import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from apps.datasets.models import Dataset

TEST_CSV_NAME = "Egor"
TEST_CSV_AGE = 22
TEST_CSV_COL_NAME = "name"
TEST_CSV_COL_AGE = "age"
TEST_CSV_COLUMNS = {TEST_CSV_COL_NAME, TEST_CSV_COL_AGE}


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="example@example.com",
        password="testpass123",
    )


@pytest.fixture
def dataset(user):
    return Dataset.objects.create(
        name="Test Dataset",
        file_type="csv",
        user=user,
        file=SimpleUploadedFile(
            "test.csv",
            f"{TEST_CSV_COL_NAME},{TEST_CSV_COL_AGE}\n{TEST_CSV_NAME},{TEST_CSV_AGE}".encode(),
            content_type="text/csv",
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
            "test.csv",
            f"{TEST_CSV_COL_NAME},{TEST_CSV_COL_AGE}\n{TEST_CSV_NAME},{TEST_CSV_AGE}".encode(),
            content_type="text/csv",
        ),
    )


@pytest.fixture
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="example2@example.com",
        password="testpass321",
    )
