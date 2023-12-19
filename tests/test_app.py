"""Tests for app.py"""
from flask.testing import FlaskClient
from flask import session
import pytest
from app import app
import app as flask_app
import config
from invoice_form import InvoiceForm
from demo_values import demo_values
import json

HTTP_SUCCESS = 200


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()


def test_get_index(client) -> None:
    response = client.get("/")
    assert response.status_code == HTTP_SUCCESS
    assert flask_app.APP_TITLE in response.text
    assert flask_app.open_in_new_tab == ('target="_blank"' in response.text)
    assert demo_values['info']['seller_name'] in response.text


def test_get_version(client) -> None:
    response = client.get("/version")
    assert response.status_code == HTTP_SUCCESS
    data = response.get_json()
    assert data["version"] == config.VERSION
    assert "timestamp" in data


def test_get_version_slash(client) -> None:
    """URL slashes are strict."""
    response = client.get("/version/")
    assert response.status_code == 404


def test_errorpage_homelink(client) -> None:
    """Check that the error page gives a link home."""
    response = client.get("/lkjhghjgcvhjkn")
    assert response.status_code == 404
    assert '<a href="/">Home</a>' in response.text


def test_post_index_no_data(client) -> None:
    response = client.post("/")
    assert response.status_code == 500


@pytest.mark.skip(reason="incomplete")
def test_post_index_demo_form(client) -> None:
    with app.test_request_context():
        form = InvoiceForm(None, **demo_values)
        print(form.data)
        response = client.post("/", data=form.data)
        assert response.status_code == 200


@pytest.mark.skip(reason="incomplete")
def test_post_indfvfex(client) -> None:
    body_data = {}
    response = client.post("/", data=body_data)
    assert response.status_code != HTTP_SUCCESS
    query_string = {"key": "value"}
    response = client.post("/", query_string=query_string)
    assert response.status_code != HTTP_SUCCESS
    headers = {}
    response = client.post("/", headers=headers)
    assert response.status_code != HTTP_SUCCESS


@pytest.mark.skip(reason="incomplete")
def test_access_session(client):
    with client:
        client.post("/auth/login", data={"username": "flask"})
        # session is still accessible
        assert session["user_id"] == 1
