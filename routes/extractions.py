from flask import Blueprint, request, current_app

from concurrent.futures import ThreadPoolExecutor

import tempfile
import uuid

from config.db import db
from config.settings import Config

from models.job import Job
from models.extracted_file import ExtractedFile

from services.job_processor import process_job_archive_extractor as process_job

extractions_bp = Blueprint("extractions_routes", __name__)

executor = ThreadPoolExecutor(max_workers=Config.CONCURRENCY)


@extractions_bp.post("/extractions")
def post_extraction():

    app = current_app._get_current_object()

    archive = request.files.get("archive")
    pattern = request.form.get("pattern")

    if not archive:
        return {"error": "archive is required"}, 400

    if not pattern:
        return {"error": "pattern is required"}, 400

    temp = tempfile.NamedTemporaryFile(delete=False)

    archive.save(temp.name)

    job_id = str(uuid.uuid4())

    db.session.add(Job(id=job_id, status="pending"))

    db.session.commit()

    executor.submit(process_job, app, job_id, temp.name, archive.filename, pattern)

    return {"job_id": job_id}, 202


@extractions_bp.get("/extractions")
def get_extractions():

    jobs = Job.query.all()

    return [{"id": job.id, "status": job.status} for job in jobs]


@extractions_bp.get("/extractions/<job_id>")
def get_extraction(job_id):

    job = db.session.get(Job, job_id)

    if not job:
        return {"error": "Job not found"}, 404

    return {"job_id": job.id, "status": job.status, "error": job.error}


@extractions_bp.get("/extractions/<job_id>/results")
def get_results(job_id):

    page = int(request.args.get("page", 1))

    limit = int(request.args.get("limit", 50))

    res = ExtractedFile.query.filter_by(job_id=job_id).all()

    if not res:
        return {"error": "Job not found"}, 404

    query = ExtractedFile.query.filter_by(job_id=job_id)

    total = query.count()

    results = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "results": [
            {
                "path": r.full_path,
                "file_name": r.file_name,
                "file_size": r.file_size,
                "nesting_depth": r.nesting_depth,
                "source_archive": r.source_archive,
                "extracted_at": r.extracted_at
            }
            for r in results
        ],
    }
