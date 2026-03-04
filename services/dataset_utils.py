import os


def get_file_type(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower()
