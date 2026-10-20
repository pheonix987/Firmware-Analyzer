from models.job import Job
from config.db import db


def test_get_job_status(client):

    job = Job(
        id="test-job-1",
        status="completed"
    )

    db.session.add(job)
    db.session.commit()

    response = client.get(
        "/extractions/test-job-1"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["job_id"] == "test-job-1"
    assert data["status"] == "completed"

def test_get_all_jobs(client):
    response = client.get("/extractions")
    assert response.json == []
    assert response.status_code == 200

def test_get_unavailable_job(client):
    response = client.get("/extractions/1234")
    assert response.json == {"error": "Job not found"}
    assert response.status_code == 404