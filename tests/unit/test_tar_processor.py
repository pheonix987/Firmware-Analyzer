from unittest.mock import patch, MagicMock
from services.tar_processor import process_tar
import io

@patch("services.tar_processor.tarfile.open")
def test_process_tar_empty_archive(mock_tarfile_open):

    mock_tar = MagicMock()

    mock_tarfile_open.return_value.__enter__.return_value = mock_tar

    mock_tar.getmembers.return_value = []

    response = process_tar(
        io.BytesIO(b""),
        "*.json"
    )

    assert response == []

@patch("services.tar_processor.process_tar")
def test_process_archive_routes_to_tgz(
    mock_process_tar
):

    fake_file = io.BytesIO(b"")

    mock_process_tar.return_value = [
        {"full_path": "config.json"}
    ]

    
@patch("services.tar_processor.tarfile.open")
def test_process_tar_with_file_path(mock_tarfile_open):

    mock_tar = MagicMock()

    mock_tarfile_open.return_value = mock_tar

    mock_tar.getmembers.return_value = []

    response = process_tar(
        "sample.tar",
        "*.json"
    )

    assert response == []

    mock_tarfile_open.assert_called_once_with(
        "sample.tar",
        "r:*"
    )


@patch("services.tar_processor.tarfile.open")
def test_process_tar_skips_directory(mock_tarfile_open):

    mock_tar = MagicMock()

    member = MagicMock()
    member.isfile.return_value = False

    mock_tar.getmembers.return_value = [member]

    mock_tarfile_open.return_value.__enter__.return_value = mock_tar

    response = process_tar(
        io.BytesIO(b""),
        "*.json"
    )

    assert response == []


@patch("services.tar_processor.tarfile.open")
def test_process_tar_matches_json(mock_tarfile_open):

    mock_tar = MagicMock()

    member = MagicMock()
    member.isfile.return_value = True
    member.name = "config.json"
    member.size = 100

    mock_tar.getmembers.return_value = [member]

    mock_tarfile_open.return_value = mock_tar

    matches = process_tar(
        io.BytesIO(b""),
        "*.json"
    )

    assert len(matches) == 1

    assert matches[0]["file_name"] == "config.json"


@patch("services.tar_processor.process_archive")
@patch("services.tar_processor.tarfile.open")
def test_process_tar_nested_archive(
    mock_tarfile_open,
    mock_process_archive
):
    mock_tar = MagicMock()
    member = MagicMock()
    member.isfile.return_value = True
    member.name = "inner.zip"
    member.size = 50
    mock_tar.getmembers.return_value = [member]
    
    nested_file = MagicMock()
    nested_file.read.return_value = b"fake zip bytes"
    mock_tar.extractfile.return_value = nested_file
    
    mock_tarfile_open.return_value = mock_tar
    mock_tar.__enter__.return_value = mock_tar
    mock_tar.__exit__.return_value = None
    
    mock_process_archive.return_value = [
        {
            "file_name": "data.json",
            "full_path": "inner.zip/data.json"
        }
    ]
    
    result = process_tar(
        io.BytesIO(b"dummy tar"),
        "*.json"
    )
    
    mock_process_archive.assert_called_once()
    assert result == [
        {
            "file_name": "data.json",
            "full_path": "inner.zip/data.json"
        }
    ]
