from flask import Flask, render_template, request, flash
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

item_columns = {'names': ['description', 'price', 'percent', 'quantity'],
                'titles': ["Item description", "Unit price ex. VAT",
                           "VAT Rate (%)", "Quantity"],
                'demos': ['Golden Widget', '100.00', '20', '1']}

#  TODO: use formtarget="_blank" to open the invoice in a new tab

@app.errorhandler(404)
def page_not_found(error):
    return (render_template("base.html", title="Page not found"), 404)

@app.get("/")
def index():
    return render_template("form.html", title="VAT invoice generator",
                           item_columns=item_columns)

@app.post("/")
def index_post():
    form_data = request.form.to_dict()
    # Todo: check that price, qty, rate are correct numbers
    data = {}
    data['seller_address'] = ", ".join(form_data['seller-address'].strip().splitlines())
    data['buyer_address_lines'] = form_data['buyer-address'].strip().splitlines()
    data['invoice_number'] = form_data['invoice-number']
    data['invoice_date'] = form_data['invoice-date']
    data['currency_code'] = form_data['currency-code']
    data['seller_name'] = form_data['seller-name']
    data['seller_vat_number'] = form_data['seller-vat-number']

    data['total_ex_vat'] = 0
    data['total_vat'] = 0
    data['invoice_items'] = []
    for item in json.loads(form_data['item-data']):
        t = {}
        t['description'] = item['description']
        t['unit_price'] = float(item['price'])
        t['qty'] = int(item['quantity'])
        t['vat_rate'] = float(item['percent'])/100.0
        t['total_ex_vat'] = t['unit_price'] * t['qty']
        data['invoice_items'].append(t)
        data['total_ex_vat'] += t['total_ex_vat']
        data['total_vat'] += (t['total_ex_vat'] * t['vat_rate'])

    data['total'] = data['total_ex_vat'] + data['total_vat']

    print(data)
    return render_template("invoice.html", **data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
