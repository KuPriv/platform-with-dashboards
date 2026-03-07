import os

import pandas as pd

SUPPORTED_EXTENSIONS = {"xlsx", "xlsm", "xls", "csv"}


def get_file_type(filename: str) -> str:
    ext = get_file_extension(filename)
    if ext == "csv":
        return "csv"
    if ext in ["xlsx", "xlsm", "xls"]:
        return "excel"
    raise ValueError(f"Тип файла не поддерживается: {ext}")


def get_file_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower()


def get_parsed_file(file) -> pd.DataFrame:
    file_type = get_file_type(file.name)
    if file_type == "csv":
        for encoding in ["utf-8-sig", "cp1251"]:
            try:
                file.seek(0)
                return pd.read_csv(file, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("Неправильная кодировка")
    if file_type == "excel":
        return pd.read_excel(file)
