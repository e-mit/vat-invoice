from datetime import datetime
from jinja2 import Environment, FileSystemLoader


vs = {}
vs['invoice_number'] = "A1024"
vs['invoice_date'] = "2023-06-20"
vs['currency_code'] = "GBP"
vs['buyer_address_lines'] = ["Billy Buyer", "9 Silly Street", "London", "NW1 1AB"]

vs['seller_name'] = "The Seller Co."
vs['seller_address'] = "123 Example Road, London, EC1A 2AJ, United Kingdom."
vs['seller_vat_number'] = "ZX98765432"

vs['invoice_items'] = []
vs['invoice_items'].append({'description': 'Golden widget',
                            'unit_price': "500.00", 'vat_rate': "0.20",
                            'qty': "1", 'total_ex_vat': "500.00"})

vs['total_ex_vat'] = "500.00"
vs['total_vat'] = "100.00"
vs['total'] = "600.00"

###################################################


def get_invoice():
    environment = Environment(loader=FileSystemLoader("."))
    template = environment.get_template("credit_note_template.html")
    return template.render(**vs)
