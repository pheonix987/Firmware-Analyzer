from datetime import datetime

from config.db import db


class ExtractedFile(db.Model):
    __tablename__ = "extracted_files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.String(36),
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    full_path = db.Column(
        db.Text,
        nullable=False
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_size = db.Column(
        db.BigInteger,
        nullable=False
    )

    nesting_depth = db.Column(
        db.Integer,
        nullable=False
    )

    source_archive = db.Column(
        db.String(255),
        nullable=False
    )

    extracted_at = db.Column(
        db.DateTime,
        default=datetime.now
    )