"""Tests for app.py. Note: run with pytest --log-cli-level=DEBUG."""
from flask.testing import FlaskClient
from app import app
import pytest
import app as flask_app
import config
from invoice_form import InvoiceForm
from demo_values import demo_values
from werkzeug.datastructures import MultiDict
from typing import Any
from bs4 import BeautifulSoup

HTTP_SUCCESS = 200
HOME_LINK = '<a href="/">Home</a>'


def add_md(name: str, obj: Any, md: MultiDict) -> None:
    if isinstance(obj, dict):
        for k in obj.keys():
            add_md(f'{name}-{k}', obj[k], md)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            add_md(f'{name}-{i}', val, md)
    else:
        if name[0] == '-':
            name = name[1:]
        md.add(name, str(obj))


def dict_to_MultiDict(d: dict[str, Any]) -> MultiDict:
    """Covert a dictionary to a MultiDict as expected by WTForms."""
    md: MultiDict = MultiDict()
    add_md('', d, md)
    return md


def get_csrf_token(html: str) -> str:
    return BeautifulSoup(html, 'html.parser').select_one(
            'input#csrf_token')['value']  # type: ignore


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()


def test_dict_to_MultiDict(client) -> None:
    with client:
        response = client.get("/")
        assert response.status_code == HTTP_SUCCESS
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert form.validate()
        assert demo_values['info']['seller_name'] == form.info.seller_name.data


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
        assert "<strong>INVOICE</strong>" in response.text
        assert (f"VAT number: {demo_values['info']['seller_vat_number']}"
                in response.text)


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
        assert "<strong>INVOICE</strong>" not in response.text
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
