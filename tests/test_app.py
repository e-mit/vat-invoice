"""Tests for app.py. Note: run with pytest --log-cli-level=DEBUG."""

from datetime import datetime, timezone, timedelta
import io

from flask.testing import FlaskClient
import pytest
from pypdf import PdfReader

from app import app
import app as flask_app
import config
from demo_values import demo_values
from test_invoice_form import dict_to_MultiDict, get_csrf_token

HTTP_SUCCESS = 200
HOME_LINK = '<a href="/">Home</a>'


def extract_pdf_as_text(pdf_data: bytes) -> str:
    fulltext = ""
    for page in PdfReader(io.BytesIO(pdf_data)).pages:
        fulltext += '\n' + page.extract_text(extraction_mode="layout")
    return fulltext


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()


def test_get_index(client) -> None:
    response = client.get("/")
    assert response.status_code == HTTP_SUCCESS
    assert flask_app.APP_TITLE in response.text
    assert flask_app.OPEN_IN_NEW_TAB == ('target="_blank"' in response.text)
    assert demo_values['info']['seller_name'] in response.text


def test_get_version(client) -> None:
    response = client.get("/version")
    assert response.status_code == HTTP_SUCCESS
    data = response.get_json()
    assert data["version"] == config.VERSION
    assert data["commit_hash"] == config.COMMIT_HASH
    time_diff = abs(datetime.fromisoformat(data["timestamp_now"])
                    - datetime.now(tz=timezone.utc))
    assert time_diff < timedelta(seconds=2)


def test_get_version_slash(client) -> None:
    """URL slashes are strict."""
    response = client.get("/version/")
    assert response.status_code == 404


def test_errorpage_homelink(client) -> None:
    """Check that the error page gives a link home."""
    response = client.get("/lkjhghjgcvhjkn")
    assert response.status_code == 404
    assert HOME_LINK in response.text


def test_post_index_no_data(client) -> None:
    response = client.post("/")
    assert response.status_code == 500


def test_post_index_demo_form(client) -> None:
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        response = client.post("/", data=md)
        assert response.status_code == HTTP_SUCCESS
        assert response.data[0:4] == b"%PDF"


def test_pdf_content(client) -> None:
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        response = client.post("/", data=md)
        assert response.status_code == HTTP_SUCCESS
        fulltext = extract_pdf_as_text(response.data)
        assert (f"Invoice Number: {demo_values['info']['invoice_number']}"
                in fulltext)
        assert (f"VAT number: {demo_values['info']['seller_vat_number']}"
                in fulltext)


def test_post_index_csrf_error(client) -> None:
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        csrf_token = get_csrf_token(response.text)
        md.add('csrf_token', csrf_token[2:])
        response = client.post("/", data=md)
        assert response.status_code == flask_app.HTTP_CSRF_ERROR
        assert HOME_LINK in response.text


def test_post_index_form_error(client) -> None:
    """In this case, there is no HTTP error but the form is returned."""
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        md.pop('info-vat_percent')
        response = client.post("/", data=md)
        assert response.status_code == HTTP_SUCCESS
        assert "<!DOCTYPE html>" in response.text
        assert flask_app.APP_TITLE in response.text


def test_post_index_exception(client) -> None:
    with client:
        response = client.post("/", data={'bad': 'yes'})
        assert response.status_code == flask_app.HTTP_INTERNAL_SERVER_ERROR
        assert HOME_LINK in response.text


def test_post_index_change_flask_key(client) -> None:
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        app.config["SECRET_KEY"] = "jhhbjji"
        response = client.post("/", data=md)
        assert response.status_code == flask_app.HTTP_CSRF_ERROR
