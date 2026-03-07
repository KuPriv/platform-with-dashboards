import pytest

from apps.dashboards.models import Widget
from apps.dashboards.services import get_widget_chart_data, validate_widget_data
from conftest import TEST_CSV_AGE, TEST_CSV_COLUMNS, TEST_CSV_NAME


@pytest.mark.django_db
def test_foreign_dataset_raises_error(user, other_user, success_dataset, datasetrow):
    with pytest.raises(ValueError, match="Нет доступа к этому датасету"):
        validate_widget_data(
            dataset=success_dataset,
            x_column="name",
            y_column="age",
            chart_type="bar",
            user=other_user,
        )


@pytest.mark.django_db
def test_dataset_is_not_ready_raises_error(user, dataset):
    with pytest.raises(ValueError, match="Датасет еще не готов"):
        validate_widget_data(
            dataset=dataset,
            x_column="name",
            y_column="age",
            chart_type="pie",
            user=user,
        )


@pytest.mark.django_db
def test_dataset_is_empty_raises_error(user, success_dataset):
    with pytest.raises(ValueError, match="Датасет не содержит данных"):
        validate_widget_data(
            dataset=success_dataset,
            x_column="name",
            y_column="age",
            chart_type="pie",
            user=user,
        )


@pytest.mark.django_db
def test_x_column_does_not_exist_raises_error(user, success_dataset, datasetrow):
    x_column = "nonexist"
    with pytest.raises(ValueError, match=f"Колонка {x_column} не найдена в датасете"):
        validate_widget_data(
            dataset=success_dataset,
            x_column="nonexist",
            y_column="age",
            chart_type="pie",
            user=user,
        )


@pytest.mark.django_db
def test_y_column_to_table_raises_error(user, success_dataset, datasetrow):
    with pytest.raises(
        ValueError, match="Поле y_column не поддерживается для типа table"
    ):
        validate_widget_data(
            dataset=success_dataset,
            x_column="name",
            y_column="age",
            chart_type=Widget.ChartType.TABLE,
            user=user,
        )


@pytest.mark.django_db
def test_y_column_does_not_exist_raises_error(user, success_dataset, datasetrow):
    y_column = "nonexist"
    with pytest.raises(ValueError, match=f"Колонка {y_column} не найдена в датасете"):
        validate_widget_data(
            dataset=success_dataset,
            x_column="name",
            y_column="nonexist",
            chart_type=Widget.ChartType.BAR,
            user=user,
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "chart_type",
    [
        Widget.ChartType.PIE,
        Widget.ChartType.BAR,
        Widget.ChartType.LINE,
    ],
)
def test_y_column_required_for_chart_type_raises_error(
    user, success_dataset, datasetrow, chart_type
):
    with pytest.raises(
        ValueError, match="Поле y_column обязательно для типа bar, line и pie"
    ):
        validate_widget_data(
            dataset=success_dataset,
            x_column="name",
            y_column="",
            chart_type=chart_type,
            user=user,
        )


@pytest.mark.django_db
def test_valid_data_parses(user, success_dataset, datasetrow):
    validate_widget_data(
        dataset=success_dataset,
        x_column="name",
        y_column="age",
        chart_type=Widget.ChartType.PIE,
        user=user,
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "chart_type",
    [
        Widget.ChartType.PIE,
        Widget.ChartType.BAR,
        Widget.ChartType.LINE,
    ],
)
def test_widget_chart_returns_labels_and_values(widget, chart_type, datasetrow):
    widget.chart_type = chart_type
    widget.save()
    chart_data = get_widget_chart_data(widget)
    assert chart_data["labels"] == [TEST_CSV_NAME]
    assert chart_data["values"] == [TEST_CSV_AGE]


@pytest.mark.django_db
def test_widget_table_return_columns_and_rows(widget, datasetrow):
    widget.chart_type = Widget.ChartType.TABLE
    widget.save()
    chart_data = get_widget_chart_data(widget)
    assert set(chart_data["columns"]) == TEST_CSV_COLUMNS
    assert len(chart_data["rows"]) == 1
    assert set(chart_data["rows"][0]) == {TEST_CSV_NAME, TEST_CSV_AGE}


@pytest.mark.django_db
def test_widget_table_with_empty_dataset(widget):
    widget.chart_type = Widget.ChartType.TABLE
    widget.save()
    chart_data = get_widget_chart_data(widget)
    assert chart_data == {"columns": [], "rows": []}
