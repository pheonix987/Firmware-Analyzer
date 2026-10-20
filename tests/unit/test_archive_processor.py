from unittest.mock import patch
import io, zipfile

from services.archive_processor import process_archive

@patch("services.zip_processor.process_zip")
@patch("services.tar_processor.process_tar")
def test_process_archive_returns_empty_for_non_archive(
    mock_process_tar,
    mock_process_zip
):

    response = process_archive(
        io.BytesIO(b""),
        "document.pdf",
        "*.json"
    )

    assert response == []

    mock_process_zip.assert_not_called()
    mock_process_tar.assert_not_called()


@patch("services.zip_processor.process_zip")
@patch("services.tar_processor.process_tar")
def test_process_archive_routes_to_zip(
    mock_process_tar,
    mock_process_zip
):

    fake_file = io.BytesIO(b"")

    mock_process_zip.return_value = [
        {"full_path": "data.json"}
    ]

    response = process_archive(
        fake_file,
        "backup.zip",
        "*.json",
        parent_path="root",
        depth=1
    )

    assert response == [
        {"full_path": "data.json"}
    ]

    mock_process_zip.assert_called_once_with(
        fake_file,
        "*.json",
        "root",
        1
    )

    mock_process_tar.assert_not_called()


@patch("services.zip_processor.process_zip")
@patch("services.tar_processor.process_tar")
def test_process_archive_routes_to_tar(
    mock_process_tar,
    mock_process_zip
):

    fake_file = io.BytesIO(b"")

    mock_process_tar.return_value = [
        {"full_path": "config.json"}
    ]

    response = process_archive(
        fake_file,
        "bundle.tar",
        "*.json"
    )

    assert response == [
        {"full_path": "config.json"}
    ]

    mock_process_tar.assert_called_once_with(
        fake_file,
        "*.json",
        "",
        0
    )

    mock_process_zip.assert_not_called()


@patch("services.zip_processor.process_zip")
@patch("services.tar_processor.process_tar")
def test_process_archive_routes_to_tar_gz(
    mock_process_tar,
    mock_process_zip
):

    fake_file = io.BytesIO(b"")

    mock_process_tar.return_value = [
        {"full_path": "config.json"}
    ]

    response = process_archive(
        fake_file,
        "bundle.tar.gz",
        "*.json"
    )

    assert response == [
        {"full_path": "config.json"}
    ]

    mock_process_tar.assert_called_once_with(
        fake_file,
        "*.json",
        "",
        0,
        "r:gz"
    )

    mock_process_zip.assert_not_called()



