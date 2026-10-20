import os, tempfile, json, zipfile

from config.db import db
from services.archive_processor import process_archive
from services.firmware_analyzer import analyze_firmware
from models.job import Job
from models.extracted_file import ExtractedFile


def process_job_archive_extractor(app, job_id, archive_path, archive_name, pattern):
    with app.app_context():

        try:

            job = db.session.get(Job, job_id)

            job.status = "running"

            db.session.commit()

            matches = process_archive(archive_path, archive_name, pattern)

            for match in matches:

                db.session.add(
                    ExtractedFile(
                        job_id=job_id,
                        full_path=match["full_path"],
                        file_name=match["file_name"],
                        file_size=match["file_size"],
                        nesting_depth=match["nesting_depth"],
                        source_archive=match["source_archive"],
                    )
                )

            job.status = "completed"

            db.session.commit()

        except Exception as e:

            job = db.session.get(Job, job_id)

            if job:

                job.status = "failed"
                job.error = str(e)

                db.session.commit()


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
