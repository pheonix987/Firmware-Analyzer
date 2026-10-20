import io
import zipfile

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
