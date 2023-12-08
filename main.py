from flask import Flask, render_template, request, flash, redirect, url_for
import json
import secrets
import decimal
from decimal import Decimal
from wtforms import Form, DateField, StringField, validators
from wtforms import DecimalField, IntegerField, TextAreaField
import datetime
from typing import Any


class BasicForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    seller_address = TextAreaField('Seller address',
                                   [validators.InputRequired()])
    buyer_address = TextAreaField('Buyer address', [validators.Optional()])
    date = DateField('Date', [validators.InputRequired()])
    price = DecimalField('Price', [validators.InputRequired(),
                                   validators.NumberRange(min=0)])
    quantity = IntegerField('Quantity', [validators.InputRequired(),
                                         validators.NumberRange(min=1)])


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

optional_form_data = ['buyer_address_lines']

#  TODO: use formtarget="_blank" to open the invoice in a new tab

demo_data: dict[str, Any] = {}
demo_data['name'] = "The Seller Co."
demo_data['date'] = datetime.datetime.now().date()
demo_data['seller_address'] = "kjhjhjh"
demo_data['buyer_address'] = "buyco"
demo_data['price'] = Decimal("2.00")
demo_data['quantity'] = 3


@app.get("/wtf")
def wtf():
    form = BasicForm(request.form, **demo_data)
    return render_template("wtf.html", form=form, title="WTForms Test")


@app.post("/wtf")
def wtf_post():
    form = BasicForm(request.form)
    form.validate()
    print(form.data)
    print(form.price.data)
    print(form.errors)
    print(form.form_errors)
    return (render_template("base.html", title="Page not found"), 404)


@app.errorhandler(404)
def page_not_found(error):
    return (render_template("base.html", title="Page not found"), 404)


@app.get("/")
def index():
    return render_template("form.html", title="VAT invoice generator")


@app.post("/")
def index_post():
    data = request.form.to_dict()
    data['seller_address_single_line'] = ", ".join(
        data['seller_address'].strip().splitlines())
    data['buyer_address_lines'] = data['buyer_address'].strip().splitlines()
    data['items'] = json.loads(data['item_data'])
    # check for missing required data:
    form_fields = list(data.keys())
    for field in optional_form_data:
        form_fields.remove(field)
    if any([not data[x] for x in form_fields]):
        flash('Please complete all required fields')
        return redirect(url_for('index'))
    # TODO: check for empty fields in "items"

    vat_rate = Decimal(data['vat_percent'])/Decimal("100")
    data['total_ex_vat'] = Decimal('0.00')
    data['total_vat'] = Decimal('0.00')
    data['invoice_items'] = []
    for item in data['items']:
        t = {}
        t['description'] = item['description']
        t['unit_price'] = round(Decimal(item['price']), 2)
        t['qty'] = int(item['quantity'])
        t['total_ex_vat'] = t['unit_price'] * t['qty']
        data['invoice_items'].append(t)
        data['total_ex_vat'] += t['total_ex_vat']
        data['total_vat'] += (t['total_ex_vat'] * vat_rate)

    data['total_vat'] = data['total_vat'].quantize(Decimal('0.01'),
                                                   rounding=decimal.ROUND_DOWN)
    data['total'] = data['total_ex_vat'] + data['total_vat']

    print(data)
    return render_template("invoice.html", **data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
