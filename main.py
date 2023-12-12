from flask import Flask, render_template, request, session
import secrets
import decimal
from decimal import Decimal
from wtforms import Form, DateField, StringField, validators, FieldList
from wtforms import DecimalField, IntegerField, TextAreaField, FormField
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta, datetime
from typing import Any

open_print_dialog = False
open_in_new_tab = False


class InvoiceInfoForm(Form):
    invoice_number = StringField('Invoice number',
                                 [validators.DataRequired()])
    invoice_date = DateField('Invoice date', [validators.InputRequired()])
    currency_code = StringField('Currency code', [validators.DataRequired()])
    vat_percent = DecimalField('VAT rate (%)', [validators.InputRequired(),
                                                validators.NumberRange(min=0)])
    seller_name = StringField('Seller name', [validators.DataRequired()])
    seller_vat_number = StringField('Seller VAT number',
                                    [validators.DataRequired()])
    seller_address = TextAreaField('Seller address',
                                   [validators.DataRequired()])
    buyer_address = TextAreaField('Buyer name and address (optional)',
                                  [validators.Optional()])


class InvoiceItemForm(Form):
    description = StringField('Description', [validators.DataRequired()])
    unit_price = DecimalField('Unit price ex. VAT',
                              [validators.InputRequired(),
                               validators.NumberRange(min=0)],
                              render_kw={"step": "0.01"})
    quantity = IntegerField('Quantity', [validators.InputRequired(),
                                         validators.NumberRange(min=1)])


class InvoiceForm(Form):
    info = FormField(InvoiceInfoForm)
    items = FieldList(FormField(InvoiceItemForm), min_entries=1)

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = secrets.token_bytes(32)
        csrf_time_limit = timedelta(minutes=30)

        @property
        def csrf_context(self):
            return session


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

#  TODO: use formtarget="_blank" to open the invoice in a new tab

demo_data: dict[str, Any] = {'info': {}, 'items': [{}]}
demo_data['info']['seller_name'] = "The Seller Co."
demo_data['info']['invoice_date'] = datetime.now().date()
demo_data['info']['seller_address'] = "123 Example Road\nLondon\nEC1A 2AB"
demo_data['info']['buyer_address'] = "A. Tester\nThe High Street\nBirmingham"
demo_data['info']['invoice_number'] = "P98765"
demo_data['info']['currency_code'] = "GBP"
demo_data['info']['seller_vat_number'] = "XY12345678"
demo_data['info']['vat_percent'] = 20
demo_data['items'][0]['description'] = "Widget"
demo_data['items'][0]['unit_price'] = Decimal("9.99")
demo_data['items'][0]['quantity'] = 2


def process_data(form_data):
    data = form_data['info']
    data['seller_address_single_line'] = ", ".join(
        data['seller_address'].strip().splitlines())
    data['buyer_address_lines'] = data['buyer_address'].strip().splitlines()

    vat_rate = Decimal(data['vat_percent'])/Decimal("100")
    data['total_ex_vat'] = Decimal('0.00')
    data['total_vat'] = Decimal('0.00')
    data['invoice_items'] = []
    for item in form_data['items']:
        t = {}
        t['description'] = item['description']
        t['unit_price'] = round(Decimal(item['unit_price']), 2)
        t['quantity'] = int(item['quantity'])
        t['total_ex_vat'] = t['unit_price'] * t['quantity']
        data['invoice_items'].append(t)
        data['total_ex_vat'] += t['total_ex_vat']
        data['total_vat'] += (t['total_ex_vat'] * vat_rate)

    data['total_vat'] = data['total_vat'].quantize(Decimal('0.01'),
                                                   rounding=decimal.ROUND_DOWN)
    data['total'] = data['total_ex_vat'] + data['total_vat']
    return data


@app.get("/")
def index_get():
    form = InvoiceForm(request.form, **demo_data)
    return render_template("form.html", form=form,
                           title="VAT invoice generator",
                           open_in_new_tab=open_in_new_tab)


@app.post("/")
def index_post():
    form = InvoiceForm(request.form)
    if form.validate():
        invoice_data = process_data(form.data)
        return render_template("invoice.html", **invoice_data,
                               open_print_dialog=open_print_dialog)
    elif form.csrf_token.errors:
        return (render_template("error.html", title="CSRF token error"), 419)
    elif form.form_errors:
        return (render_template("error.html", title="The form was inconsistent"), 422)
    elif form.errors:
        return (render_template("error.html", title="The form contained errors"), 422)
    else:
        return (render_template("error.html", title="Unknown error"), 500)


@app.errorhandler(404)
def page_not_found(error):
    return (render_template("error.html", title="Page not found"), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
