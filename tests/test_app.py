import flask
from flask.testing import FlaskClient


def test_get_index(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.get("/")
    assert res.status_code == 200


def test_post_index(app: flask.app.Flask, client: FlaskClient) -> None:
    res = client.post("/")
    assert res.status_code == 405