"""Tests for invoice.py"""
import pytest
from invoice import Invoice
import demo_values as demo
from decimal import Decimal


def test_split_address():
    assert (Invoice.split_address(" abc,\nx, xx's,\r\n, \n\n Ksk \r\n ")
            == ["abc", "x, xx's", "Ksk"])


def test_remove_decimal_zeros():
    result = Invoice.remove_decimal_zeros(Decimal("023.0200"))
    expected = "23.02"
    assert result == Decimal(expected)
    assert str(result) == expected
    result2 = Invoice.remove_decimal_zeros(Decimal("21.0"))
    expected2 = "21"
    assert result2 == Decimal(expected2)
    assert str(result2) == expected2


@pytest.fixture
def demo_invoice() -> Invoice:
    return Invoice(demo.demo_values, "invoice.html")


def test_init(demo_invoice):
    assert hasattr(demo_invoice, "info")
    assert hasattr(demo_invoice, "items")


def test_format_addresses(demo_invoice):
    demo_invoice.info['seller_address'] = " abc,\nx, xx's,\r\n, \n\n Ksk \r\n "
    demo_invoice.info['buyer_address'] = "12 Test St.,\n London \r\nAB1 2CD\n "
    demo_invoice.format_addresses()
    assert (demo_invoice.info['seller_address_single_line']
            == "abc, x, xx's, Ksk")
    assert (demo_invoice.info['buyer_address_lines']
            == ["12 Test St.", "London", "AB1 2CD"])


def test_calculate_invoice(demo_invoice):
    demo_invoice.calculate_invoice()
    assert demo_invoice.info['vat_percent'] == demo.vat_percent
    assert demo_invoice.info['total_ex_vat'] == demo.total_ex_vat
    assert demo_invoice.info['total_vat'] == demo.total_vat
    assert demo_invoice.info['total'] == demo.total


def test_render_template(demo_invoice):
    demo_invoice.calculate_invoice()
    page = demo_invoice.render(False)
    assert "<strong>INVOICE</strong>" in page
    assert f"VAT number: {demo_invoice.info['seller_vat_number']}" in page
    for k in ['vat_percent', 'total_ex_vat', 'total_vat', 'total']:
        assert str(demo_invoice.info[k]) in page
