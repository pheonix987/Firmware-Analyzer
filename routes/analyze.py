import os, tempfile, uuid
from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, current_app, request

from config.db import db
from config.settings import Config
from models.job import Job
from services.job_processor import process_job_firmware_analyzer as process_job

analyze_bp = Blueprint("analyze_routes", __name__)

executor = ThreadPoolExecutor(
    max_workers=Config.CONCURRENCY
)


@analyze_bp.post("/analyze")
def post_analysis():

    app = current_app._get_current_object()

    firmware = request.files.get("firmware")

    if not firmware:
        return {
            "error": "firmware file is required"
        }, 400

    job_id = str(uuid.uuid4())

    temp = tempfile.NamedTemporaryFile(delete=False)
    
    firmware.save(temp.name)

    job = Job(
        id=job_id,
        status="pending"
    )

    db.session.add(job)
    db.session.commit()

    executor.submit(
        process_job,
        app,
        job_id,
        temp.name
    )

    return {
        "job_id": job_id,
        "status": "pending"
    }, 202


@analyze_bp.get("/jobs/<job_id>")
def get_job_status(job_id):

    job = db.session.get(Job, job_id)

    if not job:
        return {
            "error": "job not found"
        }, 404

    return {
        "job_id": job.id,
        "status": job.status
    }, 200


import json

@analyze_bp.get("/jobs/<job_id>/results")
def get_job_results(job_id):

    job = db.session.get(Job, job_id)

    if not job:
        return {
            "error": "job not found"
        }, 404

    if job.status != "completed":
        return {
            "job_id": job.id,
            "status": job.status
        }, 202

    print("Result:", job.result)
    return {
        "job_id": job.id,
        "status": job.status,
        "summary": json.loads(job.result)
    }, 200