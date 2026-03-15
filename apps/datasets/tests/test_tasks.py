from unittest.mock import patch

import pytest

from apps.datasets.models import Dataset, DatasetRow
from apps.datasets.tasks import process_dataset


@pytest.mark.django_db
def test_proccess_dataset_returns_none_when_dataset_not_found():
    assert process_dataset(999) is None


@pytest.mark.django_db
def test_proccess_dataset_sets_success_status(dataset):
    with patch("apps.datasets.tasks.send_email.delay"):
        process_dataset(dataset.id)
    dataset.refresh_from_db()
    assert dataset.status == Dataset.Status.SUCCESS


@pytest.mark.django_db
def test_proccess_datasets_creates_dataset_rows(dataset):
    with patch("apps.datasets.tasks.send_email.delay"):
        process_dataset(dataset.id)
        rows = DatasetRow.objects.filter(dataset=dataset.id)
    assert rows.count() == 1


@pytest.mark.django_db
def test_proccess_datasets_sets_failure_status_on_error(dataset):
    with patch("apps.datasets.tasks.send_email.delay"):
        with patch("apps.datasets.tasks.get_parsed_file") as mock_task:
            mock_task.side_effect = Exception("parse error")
            process_dataset.apply(
                args=[dataset.id],
                retries=process_dataset.max_retries,
            )
    dataset.refresh_from_db()
    assert dataset.status == Dataset.Status.FAILURE
