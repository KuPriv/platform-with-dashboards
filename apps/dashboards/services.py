from apps.datasets.models import Dataset, DatasetRow

from .models import Widget


def validate_widget_data(dataset, x_column, y_column, chart_type, user) -> None:
    if user != dataset.user:
        raise ValueError("Нет доступа к этому датасету")
    if dataset.status != Dataset.Status.SUCCESS:
        raise ValueError("Датасет еще не готов")
    first_row = DatasetRow.objects.filter(dataset=dataset).first()
    if first_row is None:
        raise ValueError("Датасет не содержит данных")
    if x_column not in first_row.data:
        raise ValueError(f"Колонка {x_column} не найдена в датасете")
    if y_column and chart_type == Widget.ChartType.TABLE:
        raise ValueError("Поле y_column не поддерживается для типа table")
    if y_column and y_column not in first_row.data:
        raise ValueError(f"Колонка {y_column} не найдена в датасете")
    if not y_column and chart_type in [
        Widget.ChartType.BAR,
        Widget.ChartType.LINE,
        Widget.ChartType.PIE,
    ]:
        raise ValueError("Поле y_column обязательно для типа bar, line и pie")


def get_widget_chart_data(widget: Widget) -> dict:
    rows = DatasetRow.objects.filter(dataset=widget.dataset).values_list(
        "data", flat=True
    )
    if widget.chart_type in [
        Widget.ChartType.BAR,
        Widget.ChartType.LINE,
        Widget.ChartType.PIE,
    ]:
        labels = [row[widget.x_column] for row in rows]
        values = [row[widget.y_column] for row in rows]
        return {"labels": labels, "values": values}
    if widget.chart_type == Widget.ChartType.TABLE:
        all_rows = list(rows)
        if not all_rows:
            return {"columns": [], "rows": []}
        columns = list(all_rows[0].keys())
        rows_data = [list(row.values()) for row in all_rows]
        return {"columns": columns, "rows": rows_data}
    raise ValueError(f"Неизвестный тип графика: {widget.chart_type}")
