import pytest

from apps.dashboards.models import Dashboard, Widget
from apps.datasets.models import Dataset, DatasetRow
from apps.datasets.services import get_parsed_file


@pytest.fixture
def success_dataset(dataset):
    dataset.status = Dataset.Status.SUCCESS
    dataset.save()
    return dataset


@pytest.fixture
def datasetrow(success_dataset):
    df = get_parsed_file(success_dataset.file)
    rows = [
        DatasetRow(dataset=success_dataset, data=row.to_dict(), row_index=index)
        for (index, row) in df.iterrows()
    ]
    DatasetRow.objects.bulk_create(rows, batch_size=1000)
    success_dataset.columns = list(df.columns)
    success_dataset.save(update_fields=["columns"])
    return DatasetRow.objects.filter(dataset=success_dataset).first()


@pytest.fixture
def dashboard(user):
    return Dashboard.objects.create(name="test", user=user)


@pytest.fixture
def other_dashboard(other_user):
    return Dashboard.objects.create(name="test", user=other_user)


@pytest.fixture
def widget(success_dataset, dashboard):
    return Widget.objects.create(
        dashboard=dashboard,
        dataset=success_dataset,
        chart_type=Widget.ChartType.PIE,
        x_column="name",
        y_column="age",
    )


@pytest.fixture
def other_widget(other_dashboard, other_dataset):
    other_dataset.status = Dataset.Status.SUCCESS
    other_dataset.save()
    return Widget.objects.create(
        dashboard=other_dashboard,
        dataset=other_dataset,
        chart_type=Widget.ChartType.PIE,
        x_column="name",
        y_column="age",
    )


@pytest.fixture
def other_success_dataset(other_dataset):
    other_dataset.status = Dataset.Status.SUCCESS
    other_dataset.save()
    return other_dataset
