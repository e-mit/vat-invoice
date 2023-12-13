from flask import Flask, render_template, request
import secrets
from invoice_form import InvoiceForm
from demo_values import demo_values
from invoice import calculate_invoice

HTTP_UNPROCESSABLE_CONTENT = 422
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_CSRF_ERROR = 419

open_print_dialog = False
open_in_new_tab = False


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.get("/")
def index_get(form=None) -> str:
    if not form:
        form = InvoiceForm(None, **demo_values)
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
    elif form.csrf_token.errors:  # type: ignore
        return (render_template("error.html", title="CSRF token error"),
                HTTP_CSRF_ERROR)
    elif form.form_errors:
        return (render_template("error.html",
                                title="The form was inconsistent"),
                HTTP_UNPROCESSABLE_CONTENT)
    elif form.errors:
        return index_get(form)
    else:
        return (render_template("error.html", title="Unknown error"),
                HTTP_INTERNAL_SERVER_ERROR)


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found(error) -> tuple[str, int]:
    return (render_template("error.html", title="Page not found"),
            HTTP_NOT_FOUND)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
