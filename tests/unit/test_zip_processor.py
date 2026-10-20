from unittest.mock import MagicMock, patch
from services.zip_processor import process_zip
import io, zipfile

@patch("services.zip_processor.zipfile.ZipFile")
def test_process_zip_empty_archive(mock_zipfile):

    mock_zip = MagicMock()

    mock_zipfile.return_value.__enter__.return_value = mock_zip

    mock_zip.infolist.return_value = []

    response = process_zip(
        io.BytesIO(b""),
        "*.json"
    )

    assert response == []

    
def test_nested_zip(tmp_path):

    inner_zip = tmp_path / "inner.zip"

    with zipfile.ZipFile(inner_zip, "w") as z:
        z.writestr(
            "data.json",
            '{"name":"test"}'
        )

    outer_zip = tmp_path / "outer.zip"

    with zipfile.ZipFile(outer_zip, "w") as z:
        z.write(
            inner_zip,
            arcname="inner.zip"
        )

    matches = process_zip(
        str(outer_zip),
        "*.json"
    )

    assert len(matches) == 1