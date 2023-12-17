import os

import flask
from flask.testing import FlaskClient
import requests


def test_system(app: flask.app.Flask, client: FlaskClient) -> None:

    BASE_URL = os.environ.get("BASE_URL")
    assert BASE_URL, "Cloud Run service URL not found"

    ID_TOKEN = os.environ.get("ID_TOKEN")
    assert ID_TOKEN, "Unable to acquire an ID token"

    resp = requests.get(BASE_URL, headers={"Authorization": f"Bearer {ID_TOKEN}"})
    assert resp.status_code == 200
    assert resp.text == "Hello, World!"