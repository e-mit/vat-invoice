"""A Flask app for creating VAT invoices."""
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

APP_TITLE = "VAT invoice generator"

HTTP_UNPROCESSABLE_CONTENT = 422
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_CSRF_ERROR = 419

app = Flask(__name__)
app.logger.setLevel(os.environ.get('FLASK_LOG_LEVEL', 'WARNING'))
app.config["SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY',
                                          secrets.token_urlsafe(32))

OPEN_PRINT_DIALOG = not app.config['DEBUG']
OPEN_IN_NEW_TAB = not app.config['DEBUG']


@app.get("/")
def index_get(form=None) -> str:
    """GET the main page which contains the form for input."""
    if not form:
        form = InvoiceForm(None, **demo_values)
    app.logger.debug("Form data in index_get(): %s", form.data)
    return render_template("form.html", form=form,
                           title=APP_TITLE,
                           open_in_new_tab=OPEN_IN_NEW_TAB)


@app.post("/")
def index_post() -> str | tuple[str, int]:
    """POST for form data to be returned from main page."""
    try:
        app.logger.debug("Request form in index_post(): %s", request.form)
        form = InvoiceForm(request.form)
        if form.validate():
            invoice = Invoice(form.data, "invoice.html")
            invoice.calculate_invoice()
            return invoice.render(OPEN_PRINT_DIALOG)
        if form.csrf_token.errors:  # type: ignore
            app.logger.warning('CSRF token error')
            return (render_template("error.html", title="CSRF error"),
                    HTTP_CSRF_ERROR)
        if form.form_errors:
            app.logger.error('Form consistency errors: %s',
                             form.form_errors)
            abort(HTTP_UNPROCESSABLE_CONTENT)
        elif form.errors:
            app.logger.debug('Form field errors in: %s', form.data)
            return index_get(form)
    except Exception:  # pylint: disable=broad-except
        app.logger.error('Exception while handling form: %s', request.form)
    abort(HTTP_INTERNAL_SERVER_ERROR)


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found_error(error) -> tuple[str, int]:
    """Customize page for HTTP_NOT_FOUND."""
    return (render_template("error.html", title="Page not found"),
            error.code)


@app.errorhandler(HTTP_INTERNAL_SERVER_ERROR)
def internal_server_error(error) -> tuple[str, int]:
    """Customize page for HTTP_INTERNAL_SERVER_ERROR."""
    return (render_template("error.html", title=("An error occurred "
                            "while responding to your request.")),
            error.code)


@app.errorhandler(HTTP_UNPROCESSABLE_CONTENT)
def unprocessable_content_error(error) -> tuple[str, int]:
    """Customize page for HTTP_UNPROCESSABLE_CONTENT."""
    return (render_template("error.html", title="The form was inconsistent"),
            error.code)


@app.errorhandler(HTTPException)
def http_exception(error) -> tuple[str, int]:
    """Customize page for all other HTTP exceptions."""
    return (render_template("error.html", title=("An unknown error "
                            "occurred while responding to your request.")),
            error.code)


@app.get("/version")
def version() -> Response:
    """Check version and server response in a simple way."""
    return jsonify({
        "version": config.VERSION,
        "timestamp": str(datetime.now())
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
