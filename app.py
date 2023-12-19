from flask import Flask, render_template, request
from flask import jsonify, Response, abort
import secrets
import os
from invoice_form import InvoiceForm
from demo_values import demo_values
from invoice import Invoice
from datetime import datetime
import config
from werkzeug.exceptions import HTTPException

HTTP_UNPROCESSABLE_CONTENT = 422
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_CSRF_ERROR = 419

open_print_dialog = False
open_in_new_tab = False


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY',
                                          secrets.token_urlsafe(32))


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
        invoice = Invoice(form.data, "invoice.html")
        invoice.calculate_invoice()
        return invoice.render(open_print_dialog)
    else:
        app.logger.error('Invalid form data: %s', form)
        if form.csrf_token.errors:  # type: ignore
            return (render_template("error.html", title="CSRF token error"),
                    HTTP_CSRF_ERROR)
        elif form.form_errors:
            abort(HTTP_UNPROCESSABLE_CONTENT)
        elif form.errors:
            return index_get(form)
        else:
            abort(HTTP_INTERNAL_SERVER_ERROR)


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found_error(error) -> tuple[str, int]:
    return (render_template("error.html", title="Page not found"),
            HTTP_NOT_FOUND)


@app.errorhandler(HTTP_INTERNAL_SERVER_ERROR)
def internal_server_error(error) -> tuple[str, int]:
    return (render_template("error.html", title=("An error occurred "
                            "while responding to your request.")),
            HTTP_INTERNAL_SERVER_ERROR)


@app.errorhandler(HTTP_UNPROCESSABLE_CONTENT)
def unprocessable_content_error(error) -> tuple[str, int]:
    return (render_template("error.html", title="The form was inconsistent"),
            HTTP_UNPROCESSABLE_CONTENT)


@app.errorhandler(HTTPException)
def http_exception(error) -> tuple[str, int]:
    return (render_template("error.html", title=("An unknown error "
                            "occurred while responding to your request.")),
            error.code)


@app.get("/version")
def version() -> Response:
    return jsonify({
        "version": config.VERSION,
        "timestamp": str(datetime.now())
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
