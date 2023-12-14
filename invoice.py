"""Objects for generating the output invoice document."""
import decimal
from decimal import Decimal
from typing import Any
from copy import deepcopy
import flask


class Invoice:
    """A VAT invoice."""
    def __init__(self, invoice_data: dict[str, Any]) -> None:
        self.info = deepcopy(invoice_data['info'])
        self.items = deepcopy(invoice_data['items'])
        self.format_addresses()

    def format_addresses(self) -> None:
        self.info['seller_address_single_line'] = ", ".join(self.split_address(
            self.info['seller_address']))
        self.info['buyer_address_lines'] = self.split_address(
            self.info['buyer_address'])

    @staticmethod
    def split_address(address: str) -> list[str]:
        """Separate a multi-line address string into a list of lines."""
        address_list = [x.strip(', ') for x in address.strip().splitlines()]
        address_list = [x for x in address_list if x]
        return address_list

    @staticmethod
    def remove_decimal_zeros(d: Decimal) -> Decimal:
        """Remove insignificant zeros from a Decimal."""
        if d == d.to_integral():
            return d.quantize(Decimal(1))
        else:
            return d.normalize()

    def calculate_invoice(self) -> None:
        """Calculate line-item/invoice VAT and total amounts."""
        self.info['vat_percent'] = self.remove_decimal_zeros(
            self.info['vat_percent'])
        vat_rate = Decimal(self.info['vat_percent'])/Decimal("100")
        self.info['total_ex_vat'] = Decimal('0.00')
        self.info['total_vat'] = Decimal('0.00')
        for item in self.items:
            item['unit_price'] = item['unit_price'].quantize(Decimal('0.01'))
            item['total_ex_vat'] = item['unit_price'] * item['quantity']
            self.info['total_ex_vat'] += item['total_ex_vat']
            self.info['total_vat'] += (item['total_ex_vat'] * vat_rate)
        self.info['total_vat'] = self.info['total_vat'].quantize(
            Decimal('0.01'), rounding=decimal.ROUND_DOWN)
        self.info['total'] = self.info['total_ex_vat'] + self.info['total_vat']

    def render_template(self, template_file: str, **kwargs) -> str:
        return flask.render_template(template_file, **self.info,
                                     items=self.items, **kwargs)
