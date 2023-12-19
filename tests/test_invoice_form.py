"""Tests for invoice_form.py"""
from flask.testing import FlaskClient
from app import app
import pytest
from demo_values import demo_values
from werkzeug.datastructures import MultiDict
from typing import Any
from bs4 import BeautifulSoup
from invoice_form import InvoiceForm


def add_md(name: str, obj: Any, md: MultiDict) -> None:
    """Recursively extract items from an object and add to a flat MultiDict."""
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
    """Extract the token from the served webpage html."""
    return BeautifulSoup(html, 'html.parser').select_one(
            'input#csrf_token')['value']  # type: ignore


def test_get_csrf_token(client) -> None:
    csrf = "20231219151901##96dc18c10e830ac0862d97aa9f4de082b5154fc9"
    s = f'<input id="csrf_token" name="csrf_token" type="hidden" value="{csrf}">'
    assert get_csrf_token(s) == csrf


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()


def test_valid_invoiceform(client) -> None:
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert form.validate()
        assert demo_values['info']['seller_name'] == form.info.seller_name.data


def test_invoiceform_missing_value(client) -> None:
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', get_csrf_token(response.text))
        md.pop('info-seller_name')
        form = InvoiceForm(md)
        assert not form.validate()

