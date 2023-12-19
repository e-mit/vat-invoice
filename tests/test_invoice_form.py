"""Tests for invoice_form.py"""
from flask.testing import FlaskClient
from app import app
import pytest
from demo_values import demo_values
from werkzeug.datastructures import MultiDict
from typing import Any
from bs4 import BeautifulSoup
from invoice_form import InvoiceForm
from decimal import Decimal
from copy import deepcopy


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
    s = ('<input id="csrf_token" name="csrf_token" '
         f'type="hidden" value="{csrf}">')
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


def test_invoiceform_bad_vatnum(client) -> None:
    data = deepcopy(demo_values)
    data['info']['seller_vat_number'] = "a123"
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(data)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert not form.validate()


def test_invoiceform_bad_vatpc(client) -> None:
    data = deepcopy(demo_values)
    data['info']['vat_percent'] = Decimal("-2.3")
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(data)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert not form.validate()


def test_invoiceform_bad_csrf(client) -> None:
    with client:
        client.get("/")
        md = dict_to_MultiDict(demo_values)
        md.add('csrf_token', "12345")
        form = InvoiceForm(md)
        assert not form.validate()


def test_valid_no_buyer_address(client) -> None:
    data = deepcopy(demo_values)
    data['info']['buyer_address'] = None
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(data)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert form.validate()
        assert demo_values['info']['seller_name'] == form.info.seller_name.data


def test_stripped_strings(client) -> None:
    data = deepcopy(demo_values)
    cc = "EUR"
    inv = "9876545678"
    sa = "123 Buckingham Palace Road\nLondon"
    data['info']['currency_code'] = f" {cc} "
    data['info']['invoice_number'] = f" {inv}\n \r\n "
    data['info']['seller_address'] = f" {sa}\n \r\n "
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(data)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert form.validate()
        assert demo_values['info']['seller_name'] == form.info.seller_name.data
        assert form.info.currency_code.data == cc
        assert form.info.invoice_number.data == inv
        assert form.info.seller_address.data == sa


def test_vat_number_formatting(client) -> None:
    data = deepcopy(demo_values)
    vatnum = "ab12345"
    data['info']['seller_vat_number'] = vatnum
    with client:
        response = client.get("/")
        md = dict_to_MultiDict(data)
        md.add('csrf_token', get_csrf_token(response.text))
        form = InvoiceForm(md)
        assert form.validate()
        assert form.info.seller_vat_number.data == vatnum.upper()
