import os

import pandas as pd


def get_file_type(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower()


def get_parsed_file(file) -> pd.DataFrame:
    file_type = get_file_type(file.name)
    if file_type == "csv":
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)
