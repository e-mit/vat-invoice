"""Objects for generating the output invoice document."""
import decimal
from decimal import Decimal
from typing import Any


def split_address(address: str) -> list[str]:
    """Separate a multi-line address string into a list of lines."""
    data = [x.strip(', ') for x in
            address.strip().splitlines()]
    data = [x for x in data if x]
    return data


class InvoiceItem:
    """A product/item line on the invoice."""
    def __init__(self, description: str, unit_price: Decimal,
                 quantity: int) -> None:
        self.description = description
        self.unit_price = round(Decimal(unit_price), 2)
        self.quantity = int(quantity)
        self.total_ex_vat = self.unit_price * self.quantity


def calculate_invoice(form_data: dict[str, Any]) -> dict[str, Any]:
    """Calculate line-item and invoice VAT and total amounts."""
    data = form_data['info']
    data['seller_address_single_line'] = ", ".join(split_address(
        data['seller_address']))
    data['buyer_address_lines'] = split_address(data['buyer_address'])
    vat_rate = Decimal(data['vat_percent'])/Decimal("100")
    data['total_ex_vat'] = Decimal('0.00')
    data['total_vat'] = Decimal('0.00')
    data['invoice_items'] = []
    for item in form_data['items']:
        invoice_item = InvoiceItem(item['description'], item['unit_price'],
                                   item['quantity'])
        data['invoice_items'].append(invoice_item)
        data['total_ex_vat'] += invoice_item.total_ex_vat
        data['total_vat'] += (invoice_item.total_ex_vat * vat_rate)

    data['total_vat'] = data['total_vat'].quantize(Decimal('0.01'),
                                                   rounding=decimal.ROUND_DOWN)
    data['total'] = data['total_ex_vat'] + data['total_vat']
    return data
