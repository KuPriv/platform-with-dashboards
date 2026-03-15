import pytest

from apps.dashboards.models import Widget
from conftest import TEST_CSV_AGE, TEST_CSV_NAME

DASHBOARDS_URL = "/api/v1/dashboards/"


@pytest.mark.django_db
def test_unauthenticated_returns_401(api_client):
    response = api_client.get(DASHBOARDS_URL)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_dashboard(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.post(DASHBOARDS_URL, {"name": "test"})
    assert response.status_code == 201


@pytest.mark.django_db
def test_list_returns_only_own_dashboards(api_client, user, dashboard):
    api_client.force_authenticate(user)
    response = api_client.get(DASHBOARDS_URL)
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == dashboard.id


@pytest.mark.django_db
def test_get_not_own_dashboard_returns_error(api_client, user, other_dashboard):
    api_client.force_authenticate(user)
    response = api_client.get(f"{DASHBOARDS_URL}{other_dashboard.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_dashboard(api_client, user, dashboard):
    api_client.force_authenticate(user)
    response = api_client.delete(f"{DASHBOARDS_URL}{dashboard.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_create_widget(api_client, user, dashboard, success_dataset, datasetrow):
    api_client.force_authenticate(user)
    response = api_client.post(
        f"{DASHBOARDS_URL}{dashboard.id}/widgets/",
        {
            "dataset": success_dataset.id,
            "chart_type": Widget.ChartType.PIE,
            "x_column": "name",
            "y_column": "age",
        },
    )
    assert response.status_code == 201
    assert response.data["chart_type"] == Widget.ChartType.PIE
    assert response.data["x_column"] == "name"


@pytest.mark.django_db
def test_list_returns_only_own_widgets(api_client, user, dashboard, widget):
    api_client.force_authenticate(user)
    response = api_client.get(f"{DASHBOARDS_URL}{dashboard.id}/widgets/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == widget.id


@pytest.mark.django_db
def test_get_not_own_widget_returns_error(
    api_client, user, other_dashboard, other_widget
):
    api_client.force_authenticate(user)
    response = api_client.get(
        f"{DASHBOARDS_URL}{other_dashboard.id}/widgets/{other_widget.id}/"
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_data_action_return_right_structure_response(
    api_client, user, dashboard, widget, datasetrow
):
    api_client.force_authenticate(user)
    response = api_client.get(
        f"{DASHBOARDS_URL}{dashboard.id}/widgets/{widget.id}/data/"
    )
    assert response.data["labels"] == [TEST_CSV_NAME]
    assert response.data["values"] == [str(TEST_CSV_AGE)]


@pytest.mark.django_db
def test_invalid_data_returns_validation_error(
    api_client, user, dashboard, success_dataset
):
    api_client.force_authenticate(user)
    response = api_client.post(
        f"{DASHBOARDS_URL}{dashboard.id}/widgets/",
        {
            "dataset": success_dataset.id,
            "chart_type": Widget.ChartType.PIE,
            "x_column": "nonexist_column",
            "y_column": "age",
        },
    )
    assert response.status_code == 400
