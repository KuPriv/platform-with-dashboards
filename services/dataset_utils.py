import os

import pandas as pd


def get_file_type(filename: str) -> str:
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
        raise ValueError("Не удалось определить тип файла")
    else:
        return pd.read_excel(file)
