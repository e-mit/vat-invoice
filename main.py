from flask import Flask, render_template, request, flash
from markupsafe import escape
import credit_note

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

menu_items = ["home", "foo"]

item_columns = {'description': "Item description",
                'price': "Unit price ex. VAT", 'rate': "VAT Rate (%)",
                'quantity': "Quantity"}

#  TODO: use formtarget="_blank" to open the invoice in a new tab


@app.route("/")
def home():
    return render_template("base.html", title="The Homepage",
                           menu_items=menu_items)


@app.errorhandler(404)
def page_not_found(error):
    return (render_template("base.html", title="Page not found",
                            menu_items=menu_items), 404)


@app.get("/foo")
def foo():
    return render_template("form.html", title="VAT invoice generator",
                           menu_items=menu_items, item_columns=item_columns)


@app.post("/foo")
def foo_post():
    x = request.form
    #x = str(request.form['seller-address']).splitlines()
    try:
        x = str(x)
    except Exception:
        app.logger.error("Could not convert form data")
        x = "no data found"
    print(x)
    return credit_note.get_invoice()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
