import io
import zipfile
from unittest.mock import patch, MagicMock

from models.job import Job
from config.db import db


def test_create_analyze_job(client):

    zip_bytes = io.BytesIO()

    with zipfile.ZipFile(zip_bytes, "w") as z:
        z.writestr(
            "config.json",
            '{"token":"<Tkn999XYZABTkn>"}'
        )

    zip_bytes.seek(0)

    response = client.post(
        "/analyze",
        data={
            "firmware": (
                zip_bytes,
                "sample.zip"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 202

    data = response.get_json()

    assert "job_id" in data

    job = db.session.get(
        Job,
        data["job_id"]
    )

    assert job is not None

def test_create_extraction_without_firmware(client):

    response = client.post(
        "/analyze",
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

@patch("routes.analyze.db.session")
def test_get_job_status_success(mock_db_session, client):

    mock_job = MagicMock()
    mock_job.id = 1
    mock_job.status = "Completed"

    mock_db_session.get.return_value = mock_job
    response = client.get("/jobs/1")
    assert response.json == {
            "job_id": 1,
            "status": "Completed"
        }
    assert response.status_code == 200

def test_get_job_status_fail(client):

    response = client.get("/jobs/1")
    assert response.status_code == 404

@patch("routes.analyze.db.session")
def test_get_job_results_success(mock_db_session, client):

    mock_job = MagicMock()
    mock_job.id = 1
    mock_job.status = "completed"
    mock_job.result = '{"files": 10, "issues": 2}'

    mock_db_session.get.return_value = mock_job

    response = client.get("/jobs/1/results")

    assert response.json == {
        "job_id": 1,
        "status": "completed",
        "summary": {
            "files": 10,
            "issues": 2
        }
    }
    assert response.status_code == 200


@patch("routes.analyze.db.session")
def test_get_job_results_job_not_found(mock_db_session, client):

    mock_db_session.get.return_value = None

    response = client.get("/jobs/1/results")

    assert response.json == {
        "error": "job not found"
    }
    assert response.status_code == 404


@patch("routes.analyze.db.session")
def test_get_job_results_pending(mock_db_session, client):

    mock_job = MagicMock()
    mock_job.id = 1
    mock_job.status = "processing"

    mock_db_session.get.return_value = mock_job

    response = client.get("/jobs/1/results")

    assert response.json == {
        "job_id": 1,
        "status": "processing"
    }
    assert response.status_code == 202