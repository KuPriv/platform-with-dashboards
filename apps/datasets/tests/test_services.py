import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.datasets.services import get_file_type, get_parsed_file


def test_get_file_type_raises_for_unsupported_extension():
    with pytest.raises(ValueError, match="Тип файла не поддерживается: xlsb"):
        get_file_type("test.xlsb")


def test_get_parsed_file_parses_excel_successfully(excel_file):
    df = get_parsed_file(excel_file)
    assert set(df.columns) == {"name", "age"}
    assert df.iloc[0]["name"] == "Egor"


def test_get_parsed_file_raises_for_invalid_encoding():
    with pytest.raises(ValueError, match="Неправильная кодировка"):
        file = SimpleUploadedFile("test.csv", b"\xff\xfe\x00invalid")
        get_parsed_file(file)
