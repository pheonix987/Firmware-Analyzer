from models.job import Job
from models.extracted_file import ExtractedFile
from config.db import db


def test_get_results(client):

    job = Job(
        id="job-1",
        status="completed"
    )

    db.session.add(job)

    db.session.commit()

    db.session.add(
        ExtractedFile(
            job_id="job-1",
            full_path="config.json",
            file_name="config.json",
            file_size=100,
            nesting_depth=0,
            source_archive="root"
        )
    )

    db.session.commit()

    response = client.get(
        "/extractions/job-1/results"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total"] == 1

    assert (
        data["results"][0]["file_name"]
        == "config.json"
    )