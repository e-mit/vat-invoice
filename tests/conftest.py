import flask
from flask.testing import FlaskClient
import pytest

from app import app as flask_app


@pytest.fixture
def app() -> None:
    yield flask_app


@pytest.fixture
def client(app: flask.app.Flask) -> FlaskClient:
    return app.test_client()