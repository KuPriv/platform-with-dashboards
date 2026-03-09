import os

import pandas as pd
from django.db.models.fields.files import FieldFile

SUPPORTED_EXTENSIONS = {"xlsx", "xlsm", "xls", "csv"}
CSV_ENCODINGS = ["utf-8-sig", "cp1251"]
EXCEL_EXTENSIONS = ["xlsx", "xlsm", "xls"]


def get_file_type(filename: str) -> str:
    ext = get_file_extension(filename)
    if ext == "csv":
        return "csv"
    if ext in EXCEL_EXTENSIONS:
        return "excel"
    raise ValueError(f"Тип файла не поддерживается: {ext}")


def get_file_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower()


def get_parsed_file(file: FieldFile) -> pd.DataFrame:
    file_type = get_file_type(file.name)
    with file.open("rb") as f:
        if file_type == "csv":
            for encoding in CSV_ENCODINGS:
                try:
                    f.seek(0)
                    return pd.read_csv(f, encoding=encoding)
                except UnicodeDecodeError:
                    continue
            raise ValueError("Неправильная кодировка")
        elif file_type == "excel":
            return pd.read_excel(f)
