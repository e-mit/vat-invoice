from flask import Flask, render_template, request, session
import secrets
import decimal
from decimal import Decimal
from wtforms import Form, DateField, StringField, validators, FieldList
from wtforms import DecimalField, IntegerField, TextAreaField, FormField
from wtforms import ValidationError, Field
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta, datetime
from typing import Any

HTTP_UNPROCESSABLE_CONTENT = 422
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_CSRF_ERROR = 419

open_print_dialog = False
open_in_new_tab = False


class StrippedStringField(StringField):
    def process_formdata(self, valuelist: list[Any]) -> None:
        if valuelist:
            self.data = valuelist[0].strip()


def split_address(address: str) -> list[str]:
    """Separate a multi-line address string into a list of lines."""
    data = [x.strip(', ') for x in
            address.strip().splitlines()]
    data = [x for x in data if x]
    return data


class StrippedTextAreaField(TextAreaField):
    def process_formdata(self, valuelist: list[Any]) -> None:
        if valuelist:
            self.data = valuelist[0].strip()


class InvoiceInfoForm(Form):
    """Information not concerning the sold items."""
    invoice_number = StrippedStringField('Invoice number',
                                         [validators.DataRequired()])
    invoice_date = DateField('Invoice date', [validators.InputRequired()])
    currency_code = StrippedStringField('Currency code',
                                        [validators.DataRequired()])
    vat_percent = DecimalField('VAT rate (%)', [validators.InputRequired(),
                                                validators.NumberRange(
                                                    min=0, max=100)])
    seller_name = StrippedStringField('Seller name',
                                      [validators.DataRequired()])
    seller_vat_number = StrippedStringField('Seller VAT number',
                                            [validators.DataRequired()],
                                            filters=[str.upper])
    seller_address = StrippedTextAreaField('Seller address',
                                           [validators.DataRequired()])
    buyer_address = StrippedTextAreaField('Buyer name and address (optional)',
                                          [validators.Optional()])

    def validate_seller_vat_number(self, field: Field) -> None:
        """Do not attempt a proper validation but check for country prefix."""
        valid = (len(field.data) >= 3) and field.data[0:2].isalpha()
        if not valid:
            raise ValidationError('VAT number must start with 2 letters')


class InvoiceItemForm(Form):
    """Information for one invoice item (line item)."""
    description = StrippedStringField('Description',
                                      [validators.DataRequired()])
    unit_price = DecimalField('Unit price ex. VAT',
                              [validators.InputRequired(),
                               validators.NumberRange(min=0)],
                              render_kw={"step": "0.01"})
    quantity = IntegerField('Quantity', [validators.InputRequired(),
                                         validators.NumberRange(min=1)])


class InvoiceForm(Form):
    """The input form containing the invoice data."""
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
demo_data['items'].append({})
demo_data['items'][1]['description'] = "Delivery"
demo_data['items'][1]['unit_price'] = Decimal("4.99")
demo_data['items'][1]['quantity'] = 1


class InvoiceItem:
    def __init__(self, description: str, unit_price: Decimal,
                 quantity: int) -> None:
        self.description = description
        self.unit_price = round(Decimal(unit_price), 2)
        self.quantity = int(quantity)
        self.total_ex_vat = self.unit_price * self.quantity


def calculate_invoice(form_data: dict[str, Any]) -> dict[str, Any]:
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


@app.get("/")
def index_get(form=None) -> str:
    if not form:
        form = InvoiceForm(None, **demo_data)
    return render_template("form.html", form=form,
                           title="VAT invoice generator",
                           open_in_new_tab=open_in_new_tab)


@app.post("/")
def index_post() -> str | tuple[str, int]:
    form = InvoiceForm(request.form)
    if form.validate():
        invoice_data = calculate_invoice(form.data)
        return render_template("invoice.html", **invoice_data,
                               open_print_dialog=open_print_dialog)
    elif form.errors:
        return index_get(form)
    elif form.csrf_token.errors:  # type: ignore
        return (render_template("error.html", title="CSRF token error"),
                HTTP_CSRF_ERROR)
    elif form.form_errors:
        return (render_template("error.html",
                                title="The form was inconsistent"),
                HTTP_UNPROCESSABLE_CONTENT)
    else:
        return (render_template("error.html", title="Unknown error"),
                HTTP_INTERNAL_SERVER_ERROR)


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found(error) -> tuple[str, int]:
    return (render_template("error.html", title="Page not found"),
            HTTP_NOT_FOUND)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
