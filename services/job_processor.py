import os, tempfile, json, zipfile

from config.db import db
from services.archive_processor import process_archive
from services.firmware_analyzer import analyze_firmware
from models.job import Job
from models.extracted_file import ExtractedFile


def process_job_firmware_analyzer(app, job_id, firmware_path):
    with app.app_context():
        job = db.session.get(Job, job_id)

        with tempfile.TemporaryDirectory() as extract_dir:
            try:
                job.status = "processing"
                db.session.commit()

                with zipfile.ZipFile(firmware_path, "r") as z:
                    z.extractall(extract_dir)

                csv_path = os.path.join(
                    tempfile.gettempdir(),
                    f"{job_id}.csv"
                )

                summary = analyze_firmware(
                    extract_dir,
                    csv_path
                )

                job.status = "completed"
                job.result = json.dumps(summary)
                db.session.commit()

            except Exception as ex:
                job.status = "failed"
                job.result = str(ex)
                db.session.commit()
            finally:
                if os.path.exists(firmware_path):
                    os.remove(firmware_path)
