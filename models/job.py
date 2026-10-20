from datetime import datetime

from config.db import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.String(36),
        primary_key=True
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    result = db.Column(
        db.Text
    )

    error = db.Column(
        db.Text
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    completed_at = db.Column(
        db.DateTime
    )