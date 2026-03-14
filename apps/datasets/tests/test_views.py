from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_file_is_valid(api_client, user):
    api_client.force_authenticate(user=user)
    file = SimpleUploadedFile("test.csv", b"name,age\nEgor,22", content_type="text/csv")
    with patch("apps.datasets.views.transaction.on_commit", lambda f: f()):
        with patch("apps.datasets.views.process_dataset.delay") as mock_task:
            response = api_client.post(
                "/api/v1/datasets/", {"name": "test", "file": file}, format="multipart"
            )
    assert response.status_code == 201
    mock_task.assert_called_once()


@pytest.mark.django_db
def test_invalid_file(api_client, user):
    api_client.force_authenticate(user=user)
    file = SimpleUploadedFile("test.pdf", b"fdfgdfgfdg", content_type="application/pdf")
    response = api_client.post(
        "/api/v1/datasets/", {"name": "test", "file": file}, format="multipart"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_returns_only_own_datasets(api_client, user, dataset, other_dataset):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/v1/datasets/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == dataset.id


@pytest.mark.django_db
def test_other_dataset_is_unavailable(api_client, user, dataset, other_dataset):
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/v1/datasets/{dataset.id}/")
    assert response.status_code == 200
    response = api_client.get(f"/api/v1/datasets/{other_dataset.id}/")
    assert response.status_code == 404
