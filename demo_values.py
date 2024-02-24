"""Example values with which the end-user can auto-populate the form."""

from decimal import Decimal
from datetime import datetime
from typing import Any

demo_values: dict[str, Any] = {'info': {}, 'items': [{}]}
demo_values['info']['seller_name'] = "The Seller Co."
demo_values['info']['invoice_date'] = datetime.now().date()
demo_values['info']['seller_address'] = "123 Example Road\nLondon\nEC1A 2AB"
demo_values['info']['buyer_address'] = "A. Tester\nThe High Street\nBirmingham"
demo_values['info']['invoice_number'] = "P98765"
demo_values['info']['currency_code'] = "GBP"
demo_values['info']['seller_vat_number'] = "XY12345678"
demo_values['info']['vat_percent'] = Decimal("20")
demo_values['items'][0]['description'] = "Widget"
demo_values['items'][0]['unit_price'] = Decimal("9.99")
demo_values['items'][0]['quantity'] = 2
demo_values['items'].append({})
demo_values['items'][1]['description'] = "Delivery"
demo_values['items'][1]['unit_price'] = Decimal("4.99")
demo_values['items'][1]['quantity'] = 1

# Expected values:
vat_percent = Decimal("20")
total_ex_vat = Decimal("24.97")
total_vat = Decimal("4.99")
total = Decimal("29.96")
