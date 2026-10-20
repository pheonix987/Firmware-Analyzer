import pytest

from app import app
from config.db import db


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.app_context():

        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()