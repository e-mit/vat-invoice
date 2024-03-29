"""Define the form object(s) which pass data between front and back ends."""

import secrets
import os
from datetime import timedelta
from typing import Any

from flask import session
from wtforms import Form, DateField, StringField, validators, FieldList
from wtforms import DecimalField, IntegerField, TextAreaField, FormField
from wtforms import ValidationError, Field
from wtforms.csrf.session import SessionCSRF

CSRF_SECRET = str.encode(os.environ.get('CSRF_SECRET',
                                        secrets.token_urlsafe(32)))


class StrippedMixin:  # pylint: disable=R0903
    """A mixin to strip leading/trailing whitespace in WTForms strings."""

    def process_formdata(self, valuelist: list[Any]) -> None:
        """Override to implement the stripping."""
        if valuelist:
            self.data = valuelist[0].strip()  # pylint: disable=W0201


class StripStringField(StrippedMixin, StringField):  # pylint: disable=R0903
    """A WTForms StringField which strips leading/trailing whitespace."""


class StripTextField(StrippedMixin, TextAreaField):  # pylint: disable=R0903
    """A WTForms TextAreaField which strips leading/trailing whitespace."""


class InvoiceInfoForm(Form):
    """General information, not concerning sold product/items."""

    invoice_number = StripStringField('Invoice number',
                                      [validators.DataRequired()])
    invoice_date = DateField('Invoice date', [validators.InputRequired()])
    currency_code = StripStringField('Currency code',
                                     [validators.DataRequired()])
    vat_percent = DecimalField('VAT rate (%)', [validators.InputRequired(),
                                                validators.NumberRange(
                                                    min=0, max=100)],
                               places=None)
    seller_name = StripStringField('Seller name',
                                   [validators.DataRequired()])
    seller_vat_number = StripStringField('Seller VAT number',
                                         [validators.DataRequired()],
                                         filters=[str.upper])
    seller_address = StripTextField('Seller address',
                                    [validators.DataRequired()])
    buyer_address = StripTextField('Buyer name and address (optional)',
                                   [validators.Optional()])

    def validate_seller_vat_number(self, field: Field) -> None:
        """Do not attempt a proper validation but check for country prefix."""
        valid = (len(field.data) >= 3) and field.data[0:2].isalpha()
        if not valid:
            raise ValidationError('VAT number must start with 2 letters')


class InvoiceItemForm(Form):
    """Information for one product/item line on the invoice."""

    description = StripStringField('Description',
                                   [validators.DataRequired()])
    unit_price = DecimalField('Unit price ex. VAT',
                              [validators.InputRequired(),
                               validators.NumberRange(min=0)],
                              render_kw={"step": "0.01"})
    quantity = IntegerField('Quantity', [validators.InputRequired(),
                                         validators.NumberRange(min=1)])


class InvoiceForm(Form):
    """The entire form for collecting the invoice data."""

    info = FormField(InvoiceInfoForm)
    items = FieldList(FormField(InvoiceItemForm), min_entries=1)

    class Meta:  # pylint: disable=R0903
        """Settings for CSRF prevention."""

        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = CSRF_SECRET
        csrf_time_limit = timedelta(minutes=30)

        @property
        def csrf_context(self):
            """Store CSRF data in the flask session."""
            return session
