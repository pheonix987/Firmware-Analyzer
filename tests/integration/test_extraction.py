import io
import zipfile
import time


def test_complete_extraction_flow(client):

    zip_bytes = io.BytesIO()

    with zipfile.ZipFile(zip_bytes, "w") as z:
        z.writestr(
            "config.json",
            '{"test": true}'    
        )

    zip_bytes.seek(0)

    response = client.post(
        "/extractions",
        data={
            "archive": (
                zip_bytes,
                "sample.zip"
            ),
            "pattern": "*.json"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 202

    job_id = response.get_json()["job_id"]

    time.sleep(1)

    status_response = client.get(
        f"/extractions/{job_id}"
    )

    assert (
        status_response.get_json()["status"]
        == "completed"
    )

    results_response = client.get(
        f"/extractions/{job_id}/results"
    )

    data = results_response.get_json()

    assert data["total"] == 1

    assert (
        data["results"][0]["file_name"]
        == "config.json"
    )